function makeSearchableDropDown(originalSelectId, searchTextPlaceholder, allowMultiple = false) {
    const searchableDropdown = new SearchableDropdown(originalSelectId, allowMultiple);
    searchableDropdown.createDropdown(searchTextPlaceholder);
    return searchableDropdown;
}


class SearchableDropdown {
  constructor(originalSelectId, allowMultiple = false) {
    this.originalSelect = document.getElementById(originalSelectId);
    this.options = Array.from(this.originalSelect.children);
    this.allowMultiple = allowMultiple;
  }

  createDropdown(searchPlaceholderText) {
      const container = document.createElement('div');
      container.classList.add('dropdown-select', 'wide');
      container.tabIndex = 0;
      const span = document.createElement('span');

      span.classList.add('current');
      span.textContent = this.options[0].textContent;
      container.appendChild(span);

      const list = document.createElement('div');
      list.classList.add('list');

      const searchBoxDiv = document.createElement('div');
      searchBoxDiv.classList.add('dd-search');

      const searchBoxInput = document.createElement('input');
      searchBoxInput.type = 'text';
      searchBoxInput.id = 'txtSearchValue';
      searchBoxInput.placeholder = searchPlaceholderText;
      searchBoxInput.classList.add('dd-searchbox');
      searchBoxInput.autocomplete = 'off';
      searchBoxInput.onkeyup = () => this._filter();
      this.searchBoxInput = searchBoxInput;

      const searchBoxOptions = document.createElement('ul');
      this.searchBoxOptions = searchBoxOptions;
      this._addItemsToList(this.options);

      searchBoxDiv.appendChild(searchBoxInput);
      list.appendChild(searchBoxDiv);
      list.appendChild(searchBoxOptions);
      container.appendChild(list);
      this.newSelect = container;
      this.originalSelect.parentElement.appendChild(container);
      this.originalSelect.style.display = 'none';

      this._addOpenCloseListener();
      this._addClickOutsideListener();
      this._addOptionClickListener();
      this._addKeysListener();
  }

  _addItemsToList(items) {
    items.forEach((option, index) => this._addItemToList(option, index));

    if (!this.allowMultiple)
        this.searchBoxOptions.firstElementChild.classList.add('selected');
  }

  _addItemToList(option, index, isChecked = false) {
    const li = document.createElement('li');
    li.classList.add('option');
    li.index
    li.dataset.value = index;

    if (this.allowMultiple) {
        const div = document.createElement('div');
        div.classList.add('multiple-select-item-container')

        const p = document.createElement('p');
        p.textContent = option.textContent;
        div.appendChild(p);

        const label = document.createElement('label');
        const checkbox = document.createElement('input');
        label.classList.add('checkbox');
        label.classList.add('checkbox-option');

        checkbox.classList.add('checkbox-option');
        checkbox.type = 'checkbox';
        if (isChecked) {
            li.classList.add('selected');
            checkbox.checked = true;
        }

        label.appendChild(checkbox);
        div.append(label);

        li.appendChild(div)
    } else {
        li.textContent = option.textContent;
    }

    this.searchBoxOptions.appendChild(li);
  }

  _filter() {
      Array.from(this.searchBoxOptions.children).forEach(option => {
          if (option.textContent.toLowerCase().includes(this.searchBoxInput.value))
              option.style.display = 'block';
          else
              option.style.display = 'none';
      })
  }

    _addOpenCloseListener() {
        this.newSelect.addEventListener('click', (event) => {
            const eventList = event.target.classList;
            const parentElementList = event.target.parentElement.classList;

            if (parentElementList.contains('open') || parentElementList.contains('multiple-select-item-container')) {
                this._removeTabIndex();
                if (!this.allowMultiple)
                    this.newSelect.classList.remove('open');
                return;
            } else if (eventList.contains('dd-searchbox') || eventList.contains('checkbox-option') || event.target.tagName === 'UL') {
                return;
            }

            this.newSelect.classList.toggle('open');
            Array.from(this.searchBoxOptions.children).forEach(el => el.tabIndex = 0);
            this.searchBoxInput.focus();
        });
    }

  _addClickOutsideListener() {
    document.addEventListener('click', (event) => {
        let parent = event.target;
        while ((parent = parent.parentElement).tagName !== 'HTML') {
            if (Array.from(parent.classList).includes('dropdown-select') && this.allowMultiple) {
                    return;
            }
        }

        if (!Array.from(event.target.classList).includes('dropdown-select')) {
          this.newSelect.classList.remove('open');
          this.newSelect.removeAttribute('tabindex');
          this._removeTabIndex();
        }
        event.stopPropagation();
    });
  }

  _removeTabIndex() {
      Array.from(this.searchBoxOptions.children).forEach(el => el.removeAttribute('tabindex'));
  }

  _addOptionClickListener() {
    this.newSelect.addEventListener('click', (event) => {
        let option = event.target;
        if (!this._isValidNewSelectOption(option))
            return;

        if (this.allowMultiple) {
            const isOptionCheckbox = option.tagName === 'INPUT';
            while (option.tagName !== 'LI')
              option = option.parentElement;

            const checkbox = option.children[0].children[1].children[0];
            if (!isOptionCheckbox)
              checkbox.checked ^= 1;

            checkbox.checked ? option.classList.add('selected') : option.classList.remove('selected');
            this.originalSelect.children[option.dataset['value']].selected = checkbox.checked;

            const selected = main.getSelectValues(this.originalSelect).join(', ');
            this.newSelect.firstChild.textContent = selected ? selected : 'None';
        } else {
            Array.from(this.searchBoxOptions.children).forEach(el => el.classList.remove('selected'));
            option.classList.add('selected');
            this.newSelect.firstChild.textContent = option.textContent;
            this.originalSelect.value = this.originalSelect.children[option.dataset['value']].value;
        }
    });
  }

  _isValidNewSelectOption(option) {
      return !(option.classList.contains('dropdown-select') ||
              option.classList.contains('dd-searchbox') ||
              option.tagName === 'UL' ||
              option.tagName === 'SPAN' ||
              option.classList.contains('list'))
  }

  _addKeysListener() {
      this.newSelect.addEventListener('keydown', (event) => {
          if (!this.newSelect.classList.contains('open'))
              return;

          const item = event.target
          if (event.keyCode === 13) {
              item.click();
          } else if (event.keyCode === 27) {
              this.newSelect.click();
          } else if (event.keyCode === 37 && !!item.prevSibling) {
              item.prevSibling.focus();
          } else if (event.keyCode === 40 && !!item.nextSibling) {
              item.nextSibling.focus();
          }
      });
  }

  addOption(name) {
    if (name === '')
        return;

    name = name.toLowerCase();
    const option = document.createElement('option');
    option.value = name;
    option.innerHTML = name.capitalize();
    option.selected = true;

    this.originalSelect.appendChild(option);
    this._addItemToList(option, this.newSelect.children[1].children[1].childElementCount, true);
  }
}

export { makeSearchableDropDown, SearchableDropdown };
