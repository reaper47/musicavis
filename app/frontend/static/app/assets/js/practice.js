class Practice {
    constructor() {

    }

    sessionKeysListener(event) {
        const isCtrl = event.ctrlKey;
        const key = event.keyCode;

        if (isCtrl && key === 83) {
            event.preventDefault();
            savePractice();
        } else if (isCtrl && key === 46) {
            deletePractice();
        }
        // When <Enter> is pressed
        else if (key === 13) {
            let el = event.srcElement;
            while (el = el.parentElement) {
                 if (el && ['UL', 'TABLE'].includes(el.tagName)) {
                    addEntryOnEnter(el);
                    return;
                }
             }
        }
        // Copy text to mobile or non mobile version for Inputs
        else if (event.target.tagName === 'INPUT') {
            const elNumber = parseInt(event.target.id.split('-')[1]);

            if (event.target.parentElement.tagName === 'TD') {
                const exercise = event.target.parentElement.parentElement;
                const exerciseMobile = Array.from(document.getElementById('practice-exercises-mobile').children).filter(x => x.tagName !== 'HR')[elNumber];

                const firstRow = exerciseMobile.children[0];
                firstRow.children[1].value = exercise.children[1].children[0].value;

                const secondRow = exerciseMobile.children[1].children[0].children[0].children;
                secondRow[0].children[1].value = exercise.children[2].children[0].value;
                secondRow[1].children[1].value = exercise.children[3].children[0].value;
                secondRow[2].children[1].value = exercise.children[4].children[0].value;
            } else if (event.target.parentElement.tagName === 'DIV') {
                let exerciseMobile = event.target;
                while (exerciseMobile.id !== 'practice-exercises-mobile')
                    exerciseMobile = exerciseMobile.parentElement;

                exerciseMobile = Array.from(exerciseMobile.children).find(x => {
                    if (x.firstElementChild !== null)
                        return x.children[0].children[1].id.includes(elNumber)
                });

                const exercise = document.getElementById('practice-exercises').tBodies[0].children[elNumber];
                const secondRow = exerciseMobile.children[1].children[0].children[0];

                exercise.children[1].children[0].value = exerciseMobile.children[0].children[1].value;
                exercise.children[2].children[0].value = secondRow.children[0].children[1].value;
                exercise.children[3].children[0].value = secondRow.children[1].children[1].value;
                exercise.children[4].children[0].value = secondRow.children[2].children[1].value;
            } else {
                const el = event.target.parentElement.parentElement.parentElement;

                if (el.id.includes('mobile')) {
                    const elNotMobile = document.getElementById(el.id.split('-mobile')[0]);
                    elNotMobile.children[elNumber].children[1].children[0].value = event.target.value;
                } else if (!el.classList.contains('field-body')) {
                    const elMobile = document.getElementById(`${el.id}-mobile`);
                    elMobile.children[elNumber].children[1].children[0].value = event.target.value;
                }
            }
        }
        // Copy text to mobile or non mobile version for TextArea
        else if (event.target.tagName === 'TEXTAREA') {
            let otherEl;

            const id = event.target.parentElement.id;
            if (id.includes('mobile'))
                otherEl = document.getElementById(`${id.split('-mobile')[0]}`);
            else
                otherEl = document.getElementById(`${id}-mobile`);

            otherEl.children[0].value = event.target.value;
        }
    }

    addEntryOnEnter(el) {
        let newItemEl, newItemElMobile;

        if (el.id.includes('mobile')) {
            newItemEl = document.getElementById(el.id.split('-mobile')[0]);
            newItemElMobile = el;
        } else {
            newItemEl = el;
            newItemElMobile = document.getElementById(`${el.id}-mobile`);
        }

        addNewItem(newItemEl);
        addNewItem(newItemElMobile);
    }

    savePractice(async_ = true) {
        const xhr = new XMLHttpRequest();
        xhr.onreadystatechange = () => {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200 && async_) {
                    const json = JSON.parse(xhr.responseText);
                    refreshFields(json);

                    Array.from(document.getElementsByClassName('notification'))
                         .forEach(el => el.style.display = 'none');

                    bulmaToast.toast({
                        'message': json.toast,
                        'type': 'is-info',
                        'animate': {'in': 'fadeIn', 'out': 'fadeOut'}
                    });
                } else if (xhr.status !== 200) {
                    console.log("Error:", xhr);
                }
            }
        }

        xhr.open('POST', practiceUrl, async_);
        const formData = new FormData(document.getElementById('practice-form'));
        xhr.send(formData);
    }

    deletePractice() {
        if (!confirm('Are you sure you want to delete this practice session?'))
            return;

        const xhr = new XMLHttpRequest();
        xhr.onreadystatechange = () => {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200)
                    window.location.replace(xhr.responseText);
                else
                    console.log("Error: ", xhr);
            }
        }

        xhr.open('DELETE', practiceUrl, true);
        xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
        xhr.send(null);
    }

    refreshFields(json) {
        refresh('ul-goals', json.goals);
        refresh('ul-positives', json.positives);
        refresh('ul-improvements', json.improvements);
        refresh('practice-exercises', json.exercises);
    }

    refresh(id, elements) {
        const items = document.getElementById(id);

        if (items.tagName === 'UL') {
            const n = items.children.length;
            if (n > 1 && n !== elements.length)
                refreshList(items, elements);
        } else if (items.tagName === 'TABLE') {
            const n = items.children[1].children.length;
            if (n > 1 && n !== elements.length)
                refreshTable(items, elements);
        }
    }

    refreshList(list, newItems) {
        while (list.children.length !== 1)
            list.removeChild(list.lastChild);

        if (newItems.length) {
            list.children[0].children[1].firstElementChild.value = newItems[0];
            for (let i = 1; i < newItems.length; i++) {
                addNewItem(list);
                list.lastChild.children[1].firstElementChild.value = newItems[i];
            }
        }
    }

    refreshTable(table, newItems) {
        const tbody = table.children[1];
        while (tbody.children.length !== 1)
            tbody.removeChild(tbody.lastChild);

        if (newItems.length) {
            tbody.children[0].children[1].firstElementChild.value = newItems[0].name;
            for (let i = 1; i < newItems.length; i++) {
                addNewItem(table);
                tbody.lastChild.children[1].firstElementChild.value = newItems[i].name;
                tbody.lastChild.children[2].firstElementChild.value = newItems[i].bpm_start;
                tbody.lastChild.children[3].firstElementChild.value = newItems[i].bpm_end;
                tbody.lastChild.children[4].firstElementChild.value = newItems[i].minutes;
            }
        }
    }

    addNodeListener(node) {
        node.addEventListener('click', (event) => {
            let card = event.srcElement;
            while (!card.classList.contains('card'))
                card = card.parentNode;

            let root = card.lastElementChild;
            while (!['UL', 'TABLE'].includes(root.tagName))
                root = root.firstElementChild;
            const otherRoot = getOtherElFromScreenType(root);

            addNewItem(root);
            addNewItem(otherRoot);
        });
    }

    addNewItem(root) {
        removeFocus(lastActiveElement);

        if (root.tagName === 'UL' && !root.id.includes('exercises')) {
            const numEntries = root.children.length;
            const lastEntry = root.children[numEntries - 1];
            const newLi = lastEntry.cloneNode(true);
            const newInput = newLi.children[1].firstElementChild;

            lastEntry.children[1].firstElementChild.classList.remove('is-focused');
            updateTextInput(newInput);
            root.appendChild(newLi);
            removeNodeListener(newLi.lastElementChild);
            focusElement(newInput);
            lastActiveElement = newInput;
        } else if (root.tagName === 'UL') {
            const numEntries = root.children.length;
            const lastEntry = root.children[numEntries - 1];
            const newLi = lastEntry.cloneNode(true);

            const nextItemNumber = `<b>${parseInt(newLi.children[0].children[0].textContent.split('.')[0]) + 1}.</b>`;
            const itemNumber = newLi.children[0].children[0];
            itemNumber.innerHTML = nextItemNumber;
            lastEntry.firstElementChild.children[1].classList.remove('is-focused');

            const newExerciseInput = newLi.children[0].children[1];
            updateTextInput(newLi.children[0].children[1]);
            newExerciseInput.textContent.bold()

            for (let i = 0; i < 3; i++) {
                const input = newLi.children[1].children[0].children[0].children[i].children[1];
                updateCellInput(input);
                input.addEventListener('change', sessionKeysListener)
            }

            root.append(document.createElement('hr'))
            root.appendChild(newLi);
            removeNodeListener(newLi.firstElementChild.lastElementChild);
            focusElement(newExerciseInput);
            lastActiveElement = newExerciseInput;
        } else {
            const table = root;
            const numTr = table.tBodies[0].children.length;
            const tr = table.tBodies[0].children[numTr - 1];
            const nextTr = tr.cloneNode(true);
            const cells = nextTr.children;

            cells[0].textContent = Number(cells[0].textContent) + 1;
            for (let i = 1; i < 5; i++) {
                const input = cells[i].firstElementChild;
                updateCellInput(input);
                input.addEventListener('change', sessionKeysListener)
            }
            removeNodeListener(cells[5]);

            root.tBodies[0].appendChild(nextTr);
            tr.children[1].children[0].classList.remove('is-focused');
            focusElement(nextTr.children[1].children[0]);
            lastActiveElement = nextTr.children[1].children[0];
        }
    }

    updateTextInput(el) {
        const newId = createNewId(el.id);
        el.id = newId;
        el.name = newId;
        el.value = '';
    }

    createNewId(id) {
        const splitId = id.split('-');
        return `${splitId[0]}-${Number(splitId[1]) + 1}-${splitId[2]}`;
    }

    updateCellInput(el) {
        const newId = createNewId(el.id);
        el.id = newId;
        el.name = newId;
        el.value = el.defaultValue;
        if (!el.hasAttribute('min'))
            el.value = '';
    }

    removeNodeListener(node) {
        node.addEventListener('click', (event) => {
            let root = event.srcElement;
            while (root.tagName !== 'LI' && root.tagName !== 'TR')
                root = root.parentNode;

            if (root.parentElement.id.includes('exercises-mobile')) {
                const ul = root.parentElement;

                if (ul.childElementCount === 1) {
                    // Reset Mobile Table
                    root.firstElementChild.children[1].value = '';
                    for (let i = 0; i < 3; i++) {
                        const el = root.lastElementChild.children[0].children[0].children[0].children[1];
                        el.value = el.defaultValue;
                    }

                    // Reset Desktop Table
                    const otherTableRow = document.getElementById('practice-exercises').tBodies[0].children[0].children;
                    otherTableRow[1].children[0].value = '';
                    for (let i = 2; i < 4; i++) {
                        otherTableRow[i].children[0].value = otherTableRow[2].children[0].defaultValue;
                    }
                } else {
                    const index = Array.from(root.parentElement.children).filter(x => x.tagName !== 'HR').findIndex(x => x === root);

                    // Remove Mobile
                    const item = Array.from(ul.children).find(x => x === root);
                    const itemIndex = Array.from(ul.children).findIndex(x => x === root);

                    ul.removeChild(item);
                    if (index === 0)
                        ul.removeChild(ul.children[itemIndex]);
                    else
                        ul.removeChild(ul.children[itemIndex-1]);

                    updateIdsMobile();

                    // Remove Desktop
                    const tbody = document.getElementById('practice-exercises').tBodies[0];
                    tbody.removeChild(tbody.children[index]);
                    updateIdsDesktop(tbody);
                    Array.from(tbody.children).forEach((x, idx) => x.children[0].textContent = idx + 1);
                }
            } else if (root.tagName === 'LI') {
                const ul = root.parentElement;

                const index = Array.from(ul.children).findIndex(li => li === root);
                const otherUl = getOtherElFromScreenType(ul);
                const otherLi = otherUl.children[index]

                if (ul.childElementCount === 1) {
                    root.children[1].firstElementChild.value = '';
                    otherLi.children[1].firstElementChild.value = '';
                } else {
                    ul.removeChild(root);
                    otherUl.removeChild(otherLi);
                }
            } else {
                const tbody = root.parentElement;
                const mobile = document.getElementById('practice-exercises-mobile');

                if (tbody.childElementCount === 1) {
                    // Reset Desktop Table
                    root.children[1].firstElementChild.value = '';
                    for (let i = 2; i < 5; i++) {
                        const el = root.children[i].firstElementChild;
                        el.value = el.defaultValue;
                        updateNewIdTable(el, 0);
                    }

                    // Reset Mobile Table
                    mobile.children[0].children[0].children[1].value = '';
                    for (let i = 0; i < 3; i++) {
                        const el = mobile.children[0].children[1].children[0].children[0].children[i].children[1];
                        el.value = el.defaultValue;
                    }
                } else {
                    // Remove Desktop Version
                    tbody.removeChild(root);
                    updateIdsDesktop(tbody);

                    // Remove Mobile Version
                    const realIndex = parseInt(root.children[1].firstElementChild.id.split('-')[1]);
                    const itemIndex = Array.from(mobile.children).findIndex(x => {
                        if (x.firstElementChild !== null)
                            return x.children[0].children[1].id.includes(realIndex)
                    });

                    mobile.removeChild(mobile.children[itemIndex]);
                    if (realIndex === 0)
                        mobile.removeChild(mobile.children[itemIndex]);
                    else
                        mobile.removeChild(mobile.children[itemIndex-1]);

                    updateIdsMobile();
                }
                Array.from(tbody.children).forEach((td, index) => td.children[0].textContent = index + 1);
            }
        });
    }

    updateIdsMobile() {
        const mobile = document.getElementById('practice-exercises-mobile');
        Array.from(mobile.children).filter(x => x.tagName !== 'HR').forEach((x, idx) => {
            let idParts = x.firstElementChild.children[1].id.split('-');

            x.firstElementChild.firstElementChild.firstElementChild.innerHTML = `<b>${idx+1}.</b>`;
            x.firstElementChild.children[1].id = `${idParts[0]}-${idx}-${idParts[2]}`;

            for (let i = 0; i < 3; i++) {
                updateNewIdTable(x.children[1].firstElementChild.firstElementChild.children[i].children[1], idx);
            }
        });
    }

    updateIdsDesktop(tbody) {
        for ([idx, tr] of Array.from(tbody.children).entries()) {
            for (let i = 1; i < 5; i++) {
                updateNewIdTable(tr.children[i].firstElementChild, idx);
            }
        }
    }

    updateNewIdTable(el, idx) {
        idParts = el.id.split('-');
        newId = `${idParts[0]}-${idx}-${idParts[2]}`;
        el.id = newId;
        el.name = newId;
    }

    tabListener(key) {
        if (key === 9)
            removeFocus(lastActiveElement);
    }

    removeFocus(element) {
        if (element) {
            element.classList.remove('is-focused');
            element = null;
        }
    }

    focusElement(el) {
        el.focus();
        el.className += ' is-focused'
    }

}

export default Practice;
