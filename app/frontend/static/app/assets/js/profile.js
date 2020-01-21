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

    const http = new XMLHttpRequest();
    http.open('POST', `/add-new-instrument?name=${instrumentName}`, true);
    http.setRequestHeader('Content-type', 'text/plain');
    http.onreadystatechange = () => {
        if (http.readyState == 4 && http.status == 200) {
            if (http.responseText == 200) {
                dropdown.addOption(instrumentName);
            }
        }
    }
    http.send(null);
}

export default pushNewInstrument;
