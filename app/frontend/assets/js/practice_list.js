class PracticeList {
    init() {
        document.addEventListener('keydown', (event) => {
            const rightArrow = 39;
            const leftArrow = 37;
            let xhr = new XMLHttpRequest();

            if (event.keyCode === rightArrow) {
                xhr.open('GET', '{% if page_obj.has_previous %}{{ page_obj.previous_page_number }}{% endif %}');
                xhr.send();
            } else if (event.keyCode === leftArrow) {
                xhr.open('GET', '{% if page_obj.has_next %}{{ page_obj.next_page_number }}{% endif %}');
                xhr.send();
            }

            xhr.onreadystatechange = () => {
                if (xhr.readyState == XMLHttpRequest.DONE && xhr.status === 200) {
                    window.location.replace(xhr.responseURL);
                    document.getElementById("practice-list-grid").focus();
                } else {
                    console.log("Error: ", xhr);
                }
            }

            xhr.onerror = () => location.reload();
        })

        const practiceDates = Array.from(document.getElementsByClassName('list-item-practice-date'));
        practiceDates.forEach(span => {
            const split = span.textContent.split(',');
            span.textContent = split[0] + ',' + split[1];
        })
    }
}

export { PracticeList }
