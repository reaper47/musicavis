import initModals from './modals.js';


class Main {
    constructor(document) {
        this.document = document;
        this.originalWindowTitle = document.title;
        this.cookieNotice();
        initModals(document);
        this.initBurgers();
    }

    cookieNotice() {
        const gdprNotice = this.document.getElementById('gdpr-notice');
        if (!this.getCookie('gdpr')) {
            gdprNotice.style.display = 'block';
            this.document.getElementById('gdpr-button').addEventListener('click', () => {
                this.createCookie('gdpr', true, 31);
                gdprNotice.classList.add('animated', 'bounceOutLeft');
            });
        } else {
            gdprNotice.style.display = 'none';
        }
    }

    getCookie(name) {
        if (this.document.cookie.length > 0) {
            const cookies = this.document.cookie.split(';').map(x => x.trim())
            return cookies.find(x => x.split('=')[0] === name);
        }
        return false;
    }

    createCookie(name, value, days) {
        let expires = '';
        if (days) {
            const date = new Date();
            date.setTime(date.getTime() + (days*24*3600*1000));
            expires = `; expires=${date.toUTCString()}`;
        }
        this.document.cookie = `${name}=${value}${expires}; path=/`;
    }

    create(el, attrs, parent_el = null) {
        const element = this.document.createElement(el);
        Object.keys(attrs).forEach((attr) => element.setAttribute(attr, attrs[attr]));
        if (parent_el != null) {
            parent_el.appendChild(element);
        }
        return element;
    }

    submitFormOnEnter(form) {
        this.document.addEventListener('keydown', (event) => {
            if (event.keyCode === 13) {
                document.createElement('form').submit.call(form);
            }
        });
    }

    removeElement(id) {
        const el = this.document.getElementById(id);
        el.parentNode.removeChild(el);
    }

    startTabsWithContent() {
        const tabs = this.document.querySelectorAll('.tabs li');
        const tabsContent = this.document.querySelectorAll('.tab-content');

        const deactivateAllTabs = () => tabs.forEach(x => x.classList.remove('is-active'));
        const hideTabsContent = () => tabsContent.forEach(x => x.classList.remove('is-active'));
        const activateTabsContent = tab => tabsContent[getIndex(tab)].classList.add('is-active');
        const getIndex = el => [...el.parentElement.children].indexOf(el);

        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                deactivateAllTabs();
                hideTabsContent();
                tab.classList.add('is-active');
                activateTabsContent(tab);
            });
        });

        //tabs[0].click();
    }

    isNumberKey(evt) {
        const charCode = (evt.which) ? evt.which : event.keyCode
        if (charCode > 31 && (charCode < 48 || charCode > 57)) {
            return false;
        }
        return true;
    }

    getOtherElFromScreenType(el) {
        if (el.id.includes('mobile')) {
            return this.document.getElementById(el.id.split('-mobile')[0]);
        }
        return this.document.getElementById(`${el.id}-mobile`);
    }

    getSelectValues(select) {
        const options = Array.from(select && select.options);
        return options.flatMap(opt => opt.selected ? [opt.value || opt.text] : []);
    }

    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    initBurgers() {
        const burgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
        burgers.forEach(el => {
            el.addEventListener('click', () => {
                el.classList.toggle('is-active');
                document.getElementById(el.dataset.target).classList.toggle('is-active');
            });
        });
    }

    initNotifications() {
        this.notificationsArea = document.getElementById('notifications');
        document.addEventListener('mousedown', (event) => {
            let el = event.target;
            while (el && !el.id.includes('notification-bell')) {
                if (el.id.includes('notifications')) {
                    this.notificationsArea.classList.remove('hide');
                    return;
                }
                el = el.parentElement;
            }
            el ? this.notificationsArea.classList.toggle('hide') : this.notificationsArea.classList.add('hide');
        });

        this.notificationsList = this.notificationsArea.lastElementChild.lastElementChild.firstElementChild;
        this.notificationBadge = document.getElementById('notification-badge');
        this.noNotificationMessage = document.getElementById('no-notification');
    }

    updateNotificationsList(response, closeNotificationList = true) {
        const notifications = JSON.parse(response);
        const numberOfNotifications = notifications.names.length;

        if (Number(this.notificationBadge.textContent) === numberOfNotifications) {
            return;
        } else if (numberOfNotifications > 0) {
            this.document.title = `(${numberOfNotifications}) ${this.originalWindowTitle}`;
            this._deleteNotifications();

            this.notificationBadge.textContent = numberOfNotifications;
            this.notificationBadge.classList.remove('hide');
            this.noNotificationMessage.classList.add('hide');

            const container = this.document.createElement('ul')
            container.classList.add('notification-element')
            notifications.names.forEach((name, idx) => {
                const data = JSON.parse(notifications.data[idx]);
                if (!data.file_name) {
                    return;
                }

                if (name.includes('export_practice_task')) {
                    const li = this.document.createElement('li');
                    li.classList.add('dropdown-item');

                    const a = this.document.createElement('a');
                    a.textContent = `Your ${data.file_name.split('.')[1].toUpperCase()} file is ready. Click here to download it`;
                    a.href = `/exports/${data.file_name}`;
                    a.setAttribute('download', '');

                    li.appendChild(a);
                    container.appendChild(li);
                    this.notificationsList.appendChild(container);
                }
            });
        } else {
            this.document.title = this.originalWindowTitle;
            this._deleteNotifications();
            this.notificationBadge.textContent = 0;
            this.notificationBadge.classList.add('hide');
            this.noNotificationMessage.classList.remove('hide');
        }

        if (closeNotificationList) {
            this.notificationsArea.classList.add('hide')
        }
    }

    _deleteNotifications() {
        Array.from(this.document.getElementsByClassName('notification-element'))
             .forEach(x => x.parentElement.removeChild(x));
    }
}

export default Main;
