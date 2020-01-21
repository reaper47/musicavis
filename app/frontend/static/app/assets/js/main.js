import initModals from './modals.js';


class Main {
    constructor(document) {
        this.document = document;
        this.originalWindowTitle = document.title;
        this.cookieNotice();
        initModals(document);
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
            let cookies = this.document.cookie.split(';').map(x => x.trim())
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

    passwordStrength(fieldId) {
        const strength = {0: 'Bad', 1: 'Okay', 2: 'Good', 3: 'Very Good', 4: 'Strong'};
        const field = this.document.getElementById(fieldId);
        const meter = this.create('progress', {'id': 'password-strength-meter', 'value': 0, 'max': 4}, field.parentNode);
        const text = this.create('p', {'id': 'password-strength-text'}, field.parentNode);

        field.addEventListener('keyup', (el) => {
            const password = el.srcElement.value;
            const score = zxcvbn(password).score;
            meter.value = score;
            text.textContent = (password !== '') ? `Strength: ${strength[score]}` : '';
        });
    }

    passwordsMatch(password, password2, span) {
        if (password.value === password2.value && password2.value) {
            span.setAttribute('checked', '');
            span.removeAttribute('unchecked');
        } else {
            span.removeAttribute('checked');
            span.setAttribute('unchecked', '');
        }
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

    updateNotifications(since, notificationBadge, notificationsList, noNotificationMessage) {
        const xhr = new XMLHttpRequest();
        xhr.onreadystatechange = () => {
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                const notifications = JSON.parse(xhr.responseText);
                const numberOfNotifications = notifications.length;

                if (Number(notificationBadge.textContent) === numberOfNotifications) {
                    return;
                } else if (numberOfNotifications > 0) {
                    this.document.title = `(${numberOfNotifications}) ${originalWindowTitle}`;
                    _deleteNotifications();

                    notificationBadge.textContent = numberOfNotifications;
                    notificationBadge.classList.remove('hide');
                    noNotificationMessage.classList.add('hide');

                    const container = this.document.createElement('ul')
                    container.classList.add('notification-element')
                    notifications.forEach(x => {
                        const data = JSON.parse(x.data);
                        if (!data.file_name)
                            return;

                        if (x.name.includes('export_practice_task')) {
                            const li = this.document.createElement('li');
                            li.classList.add('dropdown-item');

                            const a = this.document.createElement('a');
                            a.textContent = `Your ${data.file_name.split('.')[1].toUpperCase()} file is ready. Click here to download it`;
                            a.href = `/exports/${data.file_name}`;

                            li.appendChild(a);
                            li.addEventListener('click', (event) => setTimeout(() => updateNotifications(since, notificationBadge, notificationsList, noNotificationMessage), 60000));
                            container.appendChild(li);
                            notificationsList.appendChild(container);
                        }
                    });
                } else {
                    this.document.title = originalWindowTitle;
                    _deleteNotifications();
                    notificationBadge.textContent = 0;
                    notificationBadge.classList.add('hide');
                    noNotificationMessage.classList.remove('hide');
                }
            }
        }

        xhr.open('GET', `/notifications?since=${since}`);
        xhr.send(null);
    }

    _deleteNotifications() {
        elementsToRemove = Array.from(this.document.getElementsByClassName('notification-element'));
        elementsToRemove.forEach(x => x.parentElement.removeChild(x));
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
        })

        tabs[0].click();
    }

    isNumberKey(evt) {
        const charCode = (evt.which) ? evt.which : event.keyCode
        if (charCode > 31 && (charCode < 48 || charCode > 57))
            return false;
        return true;
    }

    getOtherElFromScreenType(el) {
        if (el.id.includes('mobile'))
            return this.document.getElementById(el.id.split('-mobile')[0]);
        return this.document.getElementById(`${el.id}-mobile`);
    }

    getSelectValues(select) {
        const options = Array.from(select && select.options);
        return options.flatMap(opt => opt.selected ? [opt.value || opt.text] : []);
    }
}

export default Main;
