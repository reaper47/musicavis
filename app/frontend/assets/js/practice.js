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

        document.addEventListener('click', () => this.__removeFocus());
        document.getElementById('submit-practice-form').addEventListener('click', () => this.savePractice());
        document.getElementById('delete-practice-button').addEventListener('click', () => this.deletePractice());

        Object.values(document.getElementsByClassName('add-row')).forEach(node => this.__addNodeListener(node));
        Object.values(document.getElementsByClassName('remove-row')).forEach(node => this.__removeNodeListener(node));

        Array.from(document.getElementsByClassName('input-change')).forEach(x => x.addEventListener('change', (event) => this.listener(event)));
        document.addEventListener('keyup', (event) => this.listener(event));

        this.mobileExericesUl = document.getElementById('practice-exercises-mobile');
        this.mobileExericesUl.removeChild(this.mobileExericesUl.lastElementChild);

        this.initTimer();
        this.initMetronome();
    }

    savePractice() {
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
            toast({
                'message': json.toast,
                'type': 'is-info',
                'animate': {'in': 'fadeIn', 'out': 'fadeOut'}
            });

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

    listener(event) {
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
                    const otherEl = this.__getOtherContainer(el.id);
                    this.__addEntry(otherEl);
                    this.__addEntry(el);
                    break;
                }
            }
        } else if (key === 'Tab') {
            this.__removeFocus();
        } else if (['TEXTAREA', 'INPUT'].includes(event.target.tagName) || event.type === 'change') {
            const otherEl = this.__getOtherElement(event.srcElement.id);
            otherEl.value = event.target.value;
        }
    }

    __addEntry(el) {
        if (el.tagName === 'UL' && el.id === 'practice-exercises-mobile') {
            this.__removeFocus();

            const newLi = el.lastElementChild.cloneNode(true);
            newLi.children[0].children[0].textContent = `${Number(newLi.children[0].children[0].textContent.split('.')[0]) + 1}.`;
            this.__updateTextInput(newLi.children[0].children[1]);
            this.__updateCellInput(newLi.children[1].children[0].children[0].children[0].children[1]);
            this.__updateCellInput(newLi.children[1].children[0].children[0].children[1].children[1]);
            this.__updateCellInput(newLi.children[1].children[0].children[0].children[2].children[1]);

            el.appendChild(document.createElement('hr'));
            el.appendChild(newLi);
            this.__focusElement(newLi.children[0].children[1]);
            this.__removeNodeListener(newLi.children[0].children[2])
        } else if (el.tagName === 'UL') {
            this.__removeFocus();

            const newLi = el.lastElementChild.cloneNode(true);
            const childLi = newLi.children[1].children[0];
            this.__updateTextInput(childLi);

            el.appendChild(newLi);
            this.__focusElement(childLi);
            this.__removeNodeListener(newLi.lastElementChild)
        } else if (el.tagName === 'TABLE') {
            this.__removeFocus();
            const newTr = el.tBodies[0].lastElementChild.cloneNode(true);

            newTr.children[0].textContent = `${Number(newTr.children[0].textContent.split('.')[0]) + 1}.`;
            this.__updateTextInput(newTr.children[1].children[0]);
            this.__updateCellInput(newTr.children[2].children[0]);
            this.__updateCellInput(newTr.children[3].children[0]);
            this.__updateCellInput(newTr.children[4].children[0]);

            el.tBodies[0].appendChild(newTr);
            this.__focusElement(newTr.children[1].children[0]);
            this.__removeNodeListener(newTr.children[5].children[0])
        }
    }

    __focusElement(el) {
        el.focus();
        el.className += ' is-focused'
        this.lastActiveElement = el;
    }

    __removeFocus() {
        if (this.lastActiveElement) {
            this.lastActiveElement.classList.remove('is-focused');
            this.lastActiveElement = null;
        }
    }

    __getOtherElement(id) {
        if (id.includes('mobile')) {
            return document.getElementById(id.replace('id_mobile-', 'id_'));
        }
        return document.getElementById(id.replace('id_', 'id_mobile-'));
    }

    __getOtherContainer(id) {
        if (id.includes('mobile')) {
            return document.getElementById(id.replace('-mobile', ''));
        }
        return document.getElementById(`${id}-mobile`);
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
            this.__addEntry(this.__getOtherContainer(el.id));
            this.isDirty = true;
        });
    }

    __removeNodeListener(node) {
        node.addEventListener('click', (event) => {
            let root = event.srcElement.parentElement.parentElement
            if (!['LI', 'TR'].includes(root.tagName)) {
                root = root.parentElement;

                if (root.tagName === 'DIV') {
                    root = root.parentElement;
                }
            }

            let itemIndex = [...root.parentNode.children].indexOf(root);
            let otherRoot = this.__getOtherContainer(root.parentElement.id);
            if (otherRoot === null) {
                otherRoot = this.__getOtherContainer(root.parentElement.parentElement.id);
            }

            if (root.tagName === 'TABLE' || otherRoot.tagName === 'TABLE') {
                if (otherRoot.id === 'practice-exercises') {
                    let numHrElements = 0;

                    if (itemIndex !== 0) {
                        for (let el of root.parentElement.children) {
                            if (el.tagName === 'HR') {
                                numHrElements++;
                            }
                        }
                    }

                    itemIndex -= numHrElements;
                    otherRoot = otherRoot.tBodies[0]
                }
            }

            this.__removeNode(root);
            this.__removeNode(otherRoot.children[itemIndex]);
        });
    }

    __removeNode(root) {
        const children = root.parentElement.children;
        if (children.length === 1) {
            if (root.tagName === 'LI') {
                if (root.children[0].tagName === 'DIV') {
                    root.children[0].children[1].value = '';
                    root.children[1].children[0].children[0].children[0].children[1].value = 60;
                    root.children[1].children[0].children[0].children[1].children[1].value = 60;
                    root.children[1].children[0].children[0].children[2].children[1].value = 5.00;
                } else {
                    root.children[1].children[0].value = '';
                }
            } else {
                root.children[1].children[0].value = '';
                root.children[2].children[0].value = 60;
                root.children[3].children[0].value = 60;
                root.children[4].children[0].value = 5.00;
            }
            return;
        }

        const itemIndex = [...root.parentNode.children].indexOf(root);
        if (root.parentElement.classList.contains('mobile') && root.children[0].tagName === 'DIV') {
            const rootChildren = root.parentElement.children;

            for (let i = itemIndex; i < children.length; i += 2) {
                const el = children[i];
                el.children[0].children[0].textContent = `${Number(el.children[0].children[0].textContent.split('.')[0]) - 1}.`;

                this.__updateTextInput(el.children[0].children[1], true, false);
                this.__updateCellInput(el.children[1].children[0].children[0].children[0].children[1], true, false, false);
                this.__updateCellInput(el.children[1].children[0].children[0].children[1].children[1], true, false, false);
                this.__updateCellInput(el.children[1].children[0].children[0].children[2].children[1], true, false, false);
            }

            const hr = itemIndex === 0 ? rootChildren[itemIndex + 1] : rootChildren[itemIndex - 1];
            root.parentElement.removeChild(hr);
            root.parentElement.removeChild(root);
        } else {
            for (let i = itemIndex; i < children.length; i++) {
                const el = children[i];
                if (el.tagName === 'LI') {
                    this.__updateTextInput(el.children[1].children[0], true, false);
                } else {
                    el.children[0].textContent = `${Number(el.children[0].textContent.split('.')[0]) - 1}.`;
                    this.__updateTextInput(el.children[1].children[0], true, false, false);
                    this.__updateCellInput(el.children[2].children[0], true, false, false);
                    this.__updateCellInput(el.children[3].children[0], true, false, false);
                    this.__updateCellInput(el.children[4].children[0], true, false, false);
                }
            }
            root.parentElement.removeChild(root);
        }

        this.isDirty = true;
    }

    __updateTextInput(el, isIdDecreased = false, isValueWiped = true) {
        const newId = this.__createNewId(el.id, isIdDecreased);
        el.id = newId;
        el.name = newId.split('_').slice(1).join('_');
        if (isValueWiped) {
            el.value = '';
        }
    }

    __updateCellInput(el, isIdDecreased = false, isValueWiped = true, isDefaultValue = true) {
        const newId = this.__createNewId(el.id, isIdDecreased);
        el.id = newId;
        el.name = newId.split('_').slice(1).join('_');;

        if (isDefaultValue) {
            el.value = el.defaultValue;
        }

        if (!el.hasAttribute('min') && isValueWiped) {
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

    exitConfirmation() {
        if (this.isDirty) {
            return 'There are unsaved changes. All your changes will be lost if you exit.';
        }

        this.isDirty = false;
        return null;
    }

    initTimer() {
        const metronome = new Metronome();

        const metronomeTempo = document.getElementById('metronome-tempo');
        const metronomeSignature = document.getElementById('metronome-signature');
        const metronomeSubdivision = document.getElementById('metronome-subdivision');

        const metronomeStart = document.getElementById('metronome-start');
        const metronomeResume = document.getElementById('metronome-resume');
        const metronomePause = document.getElementById('metronome-pause');
        const metronomeStop = document.getElementById('metronome-stop');

        const metronomeSignature24 = document.getElementById('metronome-signature-2/4');
        const metronomeSignature34 = document.getElementById('metronome-signature-3/4');
        const metronomeSignature44 = document.getElementById('metronome-signature-4/4');
        const metronomeSignature68 = document.getElementById('metronome-signature-6/8');
        const metronomeSignature98 = document.getElementById('metronome-signature-9/8');
        const metronomeSignature128 = document.getElementById('metronome-signature-12/8');
        const signatures = [metronomeSignature24, metronomeSignature34, metronomeSignature44, metronomeSignature68, metronomeSignature98, metronomeSignature128];

        metronomeSignature.selectedIndex = 2;
        metronome.setTempo(metronomeTempo.value);
        metronome.setSignature(metronomeSignature.value);
        metronome.setSignatureVisual(document.getElementById(`metronome-signature-${metronomeSignature.value}`));
        metronome.setSubdivision(Number(metronomeSubdivision.value));
        metronome.setBarNumberElement(document.getElementById('metronome-bar-number'));

        metronomeTempo.addEventListener('change', () => metronome.setTempo(metronomeTempo.value));

        metronomeSignature.addEventListener('change', (event) => {
          const signature = event.target.value;
          metronome.setSignature(signature);
          signatures.forEach(x => x.classList.add('hide'));

          switch (signature) {
          case '2/4':
            metronomeSignature24.classList.remove('hide');
            metronome.setSignatureVisual(metronomeSignature24);
            break;
          case '3/4':
            metronomeSignature34.classList.remove('hide');
            metronome.setSignatureVisual(metronomeSignature34);
            break;
          case '4/4':
            metronomeSignature44.classList.remove('hide');
            metronome.setSignatureVisual(metronomeSignature44);
            break;
          case '6/8':
            metronomeSignature68.classList.remove('hide');
            metronome.setSignatureVisual(metronomeSignature68);
            break;
          case '9/8':
            metronomeSignature98.classList.remove('hide');
            metronome.setSignatureVisual(metronomeSignature98);
            break;
          case '12/8':
            metronomeSignature128.classList.remove('hide');
            metronome.setSignatureVisual(metronomeSignature128);
            break;
          default:
            break;
          }
        });

        metronomeSubdivision.addEventListener('change', () => metronome.setSubdivision(Number(metronomeSubdivision.value)));

        metronomeStart.addEventListener('mousedown', () => {
          metronomeStart.classList.add('hide');
          metronomePause.classList.remove('hide');
          metronomeResume.classList.add('hide');
          metronomeStop.classList.remove('hide');

          metronome.play(metronomeTempo.value, metronomeSignature.value, );
        });

        metronomeStop.addEventListener('mousedown', () => {
          metronomeStart.classList.remove('hide');
          metronomePause.classList.add('hide');
          metronomeResume.classList.add('hide');
          metronomeStop.classList.add('hide');

          metronome.stop();
        });

        metronomePause.addEventListener('mousedown', () => {
          metronomeStart.classList.add('hide');
          metronomePause.classList.add('hide');
          metronomeResume.classList.remove('hide');
          metronomeStop.classList.remove('hide');

          metronome.pause();
        });

        metronomeResume.addEventListener('mousedown', () => {
          metronomeStart.classList.add('hide');
          metronomePause.classList.remove('hide');
          metronomeResume.classList.add('hide');
          metronomeStop.classList.remove('hide');

          metronome.play(metronomeTempo.value, metronomeSignature.value, Number(metronomeSubdivision.value));
        });
    }

    initMetronome() {
        const countdown = document.getElementById('timer-countdown');
        const timerInputs = document.getElementById('timer-input');
        const elements = {'hour': document.getElementById('timer-hours'), 'minutes': document.getElementById('timer-minutes'), 'seconds': document.getElementById('timer-seconds')};
        let timer = new Timer(elements, 1000, () => document.getElementById('modal-practice-tools').classList.add('is-active'));

        const numHours = document.getElementById('timer-num-hours');
        const numMinutes = document.getElementById('timer-num-minutes');
        const numSeconds = document.getElementById('timer-num-seconds');

        const timerStart = document.getElementById('timer-start');
        const timerStop = document.getElementById('timer-stop');

        timerStart.addEventListener('mousedown', () => {
          const time = Number(numHours.value)*3600 + Number(numMinutes.value)*60 + Number(numSeconds.value);

          timerStart.classList.add('hide');
          timerStop.classList.remove('hide');
          countdown.classList.remove('hide');
          timerInputs.classList.add('hide');

          timer.start(time);
        });

        timerStop.addEventListener('mousedown', () => {
          timerStart.classList.remove('hide');
          timerStop.classList.add('hide');
          countdown.classList.add('hide')
          timerInputs.classList.remove('hide');

          timer.stop();
        });
    }
}

export { Practice, makeSearchableDropDown, SearchableDropdown };
