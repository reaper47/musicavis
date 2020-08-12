import { makeSearchableDropDown, SearchableDropdown } from './dropdown';

function setUpExportPractice(urlExportPractices) {
    const searchableDropdown = new SearchableDropdown('id_filetype');
    searchableDropdown.createDropdown('Search for a format...');

    document.getElementById('submit-export').addEventListener('click', (event) => {
        event.preventDefault();

        fetch(new Request(urlExportPractices, {
            method: 'POST',
            mode: 'same-origin',
            headers: {'X-CSRFToken': main.getCsrfToken()},
            body: JSON.stringify({'file_type': document.getElementById('id_filetype').value})
        })).then(() => toast({
            'message': 'We are exporting your practices. Please wait.',
            'duration': 3000,
            'type': 'is-info',
            'animate': {'in': 'fadeIn', 'out': 'fadeOut'}
        }));
    });
}

export { setUpExportPractice, makeSearchableDropDown };
