import { makeSearchableDropDown, SearchableDropdown } from './dropdown';
import Main from './main';

function pushNewInstrument(newInstrumentInput, addButton, addInstrument, dropdown) {
    const instrumentName = newInstrumentInput.value;
    if (instrumentName === '') {
        newInstrumentInput.focus();
        return;
    }

    addButton.classList.add('hide');
    newInstrumentInput.classList.add('hide');
    newInstrumentInput.value = '';
    addInstrument.classList.remove('hide');

    fetch(new Request('/add-new-instrument/', {
        method: 'POST',
        mode: 'same-origin',
        headers: {'X-CSRFToken': main.getCsrfToken()},
        body: JSON.stringify({'name': instrumentName})
    })).then(() => dropdown.addOption(instrumentName));
}


function settingsPracticeLoad() {
    const searchableDropDown = makeSearchableDropDown('id_instruments', 'Search for an instrument...', true);

    const confirmAddInstrument = document.getElementById('confirm-add-instrument');
    const addInstrument = document.getElementById('add-instrument');
    const newInstrumentInput = document.getElementById('new-instrument');

    newInstrumentInput.addEventListener('keydown', (event) => {
        if (event.code === 'Enter') {
            event.preventDefault();
            pushNewInstrument(newInstrumentInput, confirmAddInstrument, addInstrument, searchableDropDown);
        }
    });

    addInstrument.addEventListener('click', () => {
        confirmAddInstrument.classList.remove('hide');
        addInstrument.classList.add('hide');
        newInstrumentInput.classList.remove('hide');
        newInstrumentInput.focus();
    });

    confirmAddInstrument.addEventListener('click', () => pushNewInstrument(newInstrumentInput, confirmAddInstrument, addInstrument, searchableDropDown));
}

export { makeSearchableDropDown, SearchableDropdown, pushNewInstrument, settingsPracticeLoad };
