class PracticeList {
    constructor(urlPractice) {
        this.url = urlPractice
    }

    init() {
        this.date = document.getElementsByClassName('month')[0].textContent.split(' ');

        this.__add_keys_listener();
        this.__add_buttons_listener();

        const practiceDates = Array.from(document.getElementsByClassName('list-item-practice-date'));
        practiceDates.forEach(span => {
            const split = span.textContent.split(',');
            span.textContent = split[0] + ',' + split[1];
        });

        this.__move_table()
    }

    __add_keys_listener() {
        document.addEventListener('keydown', (event) => {
            if (event.code === 'ArrowRight') {
                this.__get_next_month();
            } else if (event.code === 'ArrowLeft') {
                this.__get_previous_month();
            }
        });
    }

    __add_buttons_listener() {
        document.getElementById('button-month-next').addEventListener('click', () => this.__get_next_month());
        document.getElementById('button-month-previous').addEventListener('click', () => this.__get_previous_month());
    }

    __get_next_month() {
        this.setGetParam('month', this.date[0]);
        this.setGetParam('year', this.date[1]);
        this.setGetParam('flow', 'next');
        fetch(new Request(this.url));
    }

    __get_previous_month() {
        this.setGetParam('month', this.date[0]);
        this.setGetParam('year', this.date[1]);
        this.setGetParam('flow', 'previous');
        fetch(new Request(this.url));
    }

    setGetParam(key, value) {
        if (history.pushState) {
            const params = new URLSearchParams(window.location.search);
            params.set(key, value);

            const newUrl = window.location.protocol + "//" + window.location.host + window.location.pathname + '?' + params.toString();
            window.history.pushState({ path: newUrl }, '', newUrl);
        }
    }

    __move_table() {
        const table = document.querySelector('table');
        table.parentElement.appendChild(document.getElementById('calendar-buttons'));
        table.parentElement.appendChild(document.querySelector('footer'));
    }
}

export { PracticeList }
