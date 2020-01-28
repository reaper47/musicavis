import { makeSearchableDropDown, SearchableDropdown } from './dropdown';
import { Timer, Metronome } from './tools.js'


class Practice {
    constructor(practiceUrl) {
        this.lastActiveElement = null;
        this.practiceUrl = practiceUrl;
        this.isDirty = false;
    }

    init() {
        main.startTabsWithContent();

        document.addEventListener('click', () => this.__removeFocus(this.lastActiveElement));
        document.getElementById('submit-practice-form').addEventListener('click', () => this.savePractice());
        document.getElementById('delete-practice-button').addEventListener('click', () => this.deletePractice());

        Object.values(document.getElementsByClassName('add-row')).forEach(node => this.__addNodeListener(node));
        Object.values(document.getElementsByClassName('remove-row')).forEach(node => this.__removeNodeListener(node));

        Array.from(document.getElementsByClassName('change-listener')).forEach(x => x.addEventListener('change', this.sessionKeysListener));
        document.addEventListener('keyup', (event) => this.sessionKeysListener(event));
    }

    savePractice(async_ = true) {
        if (!this.isDirty) {
            return;
        }

        fetch(new Request(this.practiceUrl, {
            method: 'POST',
            mode: 'same-origin',
            body: new FormData(document.getElementById('practice-form'))
        }))
        .then(response => response.json())
        .then(json => {
            if (async_) {
                toast({
                    'message': json.toast,
                    'type': 'is-info',
                    'animate': {'in': 'fadeIn', 'out': 'fadeOut'}
                });
            }

            this.isDirty = false;
        });
    }

    deletePractice() {
        if (confirm('Are you sure you want to delete this practice session?')) {
            fetch(new Request(this.practiceUrl, {
                method: 'DELETE',
                mode: 'same-origin',
                headers: {'X-CSRFToken': main.getCsrfToken()}
            }))
            .then(response => window.location.replace(response.url))
        }
    }

    sessionKeysListener(event) {
        const isAlt = event.altKey;
        const key = event.code;
        this.isDirty = true;

        if (isAlt && key === 'KeyS') {
            this.savePractice();
        } else if (isAlt && key === 'Delete') {
            this.deletePractice();
        } else if (key === 'Enter') {
            for (let el = event.srcElement; el = el.parentElement;) {
                if (['UL', 'TABLE'].includes(el.tagName)) {
                    return this.__addEntry(el);
                }
            }
        } else if (key === 'Tab') {
            this.__removeFocus(this.lastActiveElement);
        }
    }

    __addEntry(el) {
        if (el.tagName === 'UL') {
            const newLi = el.lastElementChild.cloneNode(true);
            const childLi = newLi.children[1].children[0];
            this.__updateTextInput(childLi);
            el.appendChild(newLi);
        } else if (el.tagName === 'TABLE') {
            const newTr = el.tBodies[0].lastElementChild.cloneNode(true);

            newTr.children[0].textContent = `${Number(newTr.children[0].textContent.split('.')[0]) + 1}.`;
            this.__updateTextInput(newTr.children[1].children[0]);
            this.__updateCellInput(newTr.children[2].children[0]);
            this.__updateCellInput(newTr.children[3].children[0]);
            this.__updateCellInput(newTr.children[4].children[0]);

            el.tBodies[0].appendChild(newTr);
        }
    }

    __addNodeListener(node) {
        node.addEventListener('click', (event) => {
            let el = event.srcElement;
            while (el.tagName !== 'HEADER') {
                el = el.parentElement;
            }

            el = el.parentElement.children[1].children[0].children[0];
            if (el.tagName !== 'UL') {
                el = el.children[0]
            }

            this.__addEntry(el);
            this.isDirty = true;
        });
    }

    __removeNodeListener(node) {
        node.addEventListener('click', (event) => {
            let root = event.srcElement.parentElement.parentElement;
            if (!['LI', 'TR'].includes(root.tagName)) {
                root = root.parentElement;
            }

            const children = root.parentElement.children;
            if (children.length === 1) {
                if (root.tagName === 'LI') {
                    root.children[1].children[0].value = '';
                }
                return;
            }

            const itemIndex = [...root.parentNode.children].indexOf(root);
            for (let i = itemIndex; i < children.length; i++) {
                const el = children[i];
                if (el.tagName === 'LI') {
                    console.log(el, el.children[1].children[0].id)
                    this.__updateTextInput(el.children[1].children[0], true, false);
                } else {

                }
            }

            root.parentElement.removeChild(root);
            this.isDirty = true;
        });
    }

    __updateTextInput(el, isIdDecreased = false, isValueWiped = true) {
        const newId = this.__createNewId(el.id, isIdDecreased);
        el.id = newId;
        el.name = newId;
        if (isValueWiped) {
            el.value = '';
        }
    }

    __updateCellInput(el) {
        const newId = this.__createNewId(el.id);
        el.id = newId;
        el.name = newId;
        el.value = el.defaultValue;
        if (!el.hasAttribute('min')) {
            el.value = '';
        }
    }

    __createNewId(id, isIdDecreased = false) {
        const splitId = id.split('_');
        if (isIdDecreased) {
            splitId[2] = Number(splitId[2]) - 1;
        } else {
            splitId[2] = Number(splitId[2]) + 1;
        }
        return splitId.join('_');
    }

    __focusElement(el) {
        el.focus();
        el.className += ' is-focused'
    }

    __removeFocus(element) {
        if (element) {
            element.classList.remove('is-focused');
            element = null;
        }
    }

    exitConfirmation() {
        if (this.isDirty) {
            return 'There are unsaved changes. All your changes will be lost if you exit.';
        }

        this.isDirty = false;
        return null;
    }
}

export { Practice, makeSearchableDropDown, SearchableDropdown, Timer, Metronome };
