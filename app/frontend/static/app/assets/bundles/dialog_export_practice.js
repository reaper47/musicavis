!function(e,t){for(var n in t)e[n]=t[n]}(window,function(e){var t={};function n(i){if(t[i])return t[i].exports;var a=t[i]={i:i,l:!1,exports:{}};return e[i].call(a.exports,a,a.exports,n),a.l=!0,a.exports}return n.m=e,n.c=t,n.d=function(e,t,i){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:i})},n.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var i=Object.create(null);if(n.r(i),Object.defineProperty(i,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var a in e)n.d(i,a,function(t){return e[t]}.bind(null,a));return i},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="/static/assets/bundles/",n(n.s=18)}({0:function(e,t,n){"use strict";function i(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function a(e,t){for(var n=0;n<t.length;n++){var i=t[n];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(e,i.key,i)}}function r(e,t){var n=arguments.length>2&&void 0!==arguments[2]&&arguments[2],i=new o(e,n);return i.createDropdown(t),i}n.d(t,"b",(function(){return r})),n.d(t,"a",(function(){return o}));var o=function(){function e(t){var n=arguments.length>1&&void 0!==arguments[1]&&arguments[1];i(this,e),this.originalSelect=document.getElementById(t),this.options=Array.from(this.originalSelect.children),this.allowMultiple=n}var t,n,r;return t=e,(n=[{key:"createDropdown",value:function(e){var t=this,n=document.createElement("div");n.classList.add("dropdown-select","wide"),n.tabIndex=0;var i=document.createElement("span");i.classList.add("current"),i.textContent=this.options[0].textContent,n.appendChild(i);var a=document.createElement("div");a.classList.add("list");var r=document.createElement("div");r.classList.add("dd-search");var o=document.createElement("input");o.type="text",o.id="txtSearchValue",o.placeholder=e,o.classList.add("dd-searchbox"),o.autocomplete="off",o.onkeyup=function(){return t._filter()},this.searchBoxInput=o;var c=document.createElement("ul");this.searchBoxOptions=c,this._addItemsToList(this.options),r.appendChild(o),a.appendChild(r),a.appendChild(c),n.appendChild(a),this.newSelect=n,this.originalSelect.parentElement.appendChild(n),this.originalSelect.style.display="none",this._addOpenCloseListener(),this._addClickOutsideListener(),this._addOptionClickListener(),this._addKeysListener()}},{key:"_addItemsToList",value:function(e){var t=this;e.forEach((function(e,n){return t._addItemToList(e,n)})),this.allowMultiple||this.searchBoxOptions.firstElementChild.classList.add("selected")}},{key:"_addItemToList",value:function(e,t){var n=arguments.length>2&&void 0!==arguments[2]&&arguments[2],i=document.createElement("li");if(i.classList.add("option"),i.index,i.dataset.value=t,this.allowMultiple){var a=document.createElement("div");a.classList.add("multiple-select-item-container");var r=document.createElement("p");r.textContent=e.textContent,a.appendChild(r);var o=document.createElement("label"),c=document.createElement("input");o.classList.add("checkbox"),o.classList.add("checkbox-option"),c.classList.add("checkbox-option"),c.type="checkbox",n&&(i.classList.add("selected"),c.checked=!0),o.appendChild(c),a.append(o),i.appendChild(a)}else i.textContent=e.textContent;this.searchBoxOptions.appendChild(i)}},{key:"_filter",value:function(){var e=this;Array.from(this.searchBoxOptions.children).forEach((function(t){t.textContent.toLowerCase().includes(e.searchBoxInput.value)?t.style.display="block":t.style.display="none"}))}},{key:"_addOpenCloseListener",value:function(){var e=this;this.newSelect.addEventListener("click",(function(t){var n=t.target.classList,i=t.target.parentElement.classList;if(i.contains("open")||i.contains("multiple-select-item-container"))return e._removeTabIndex(),void(e.allowMultiple||e.newSelect.classList.remove("open"));n.contains("dd-searchbox")||n.contains("checkbox-option")||"UL"===t.target.tagName||(e.newSelect.classList.toggle("open"),Array.from(e.searchBoxOptions.children).forEach((function(e){return e.tabIndex=0})),e.searchBoxInput.focus())}))}},{key:"_addClickOutsideListener",value:function(){var e=this;document.addEventListener("click",(function(t){for(var n=t.target;"HTML"!==(n=n.parentElement).tagName;)if(Array.from(n.classList).includes("dropdown-select")&&e.allowMultiple)return;Array.from(t.target.classList).includes("dropdown-select")||(e.newSelect.classList.remove("open"),e.newSelect.removeAttribute("tabindex"),e._removeTabIndex()),t.stopPropagation()}))}},{key:"_removeTabIndex",value:function(){Array.from(this.searchBoxOptions.children).forEach((function(e){return e.removeAttribute("tabindex")}))}},{key:"_addOptionClickListener",value:function(){var e=this;this.newSelect.addEventListener("click",(function(t){var n=t.target;if(e._isValidNewSelectOption(n))if(e.allowMultiple){for(var i="INPUT"===n.tagName;"LI"!==n.tagName;)n=n.parentElement;var a=n.children[0].children[1].children[0];i||(a.checked^=1),a.checked?n.classList.add("selected"):n.classList.remove("selected"),e.originalSelect.children[n.dataset.value].selected=a.checked;var r=main.getSelectValues(e.originalSelect).join(", ");e.newSelect.firstChild.textContent=r||"None"}else Array.from(e.searchBoxOptions.children).forEach((function(e){return e.classList.remove("selected")})),n.classList.add("selected"),e.newSelect.firstChild.textContent=n.textContent,e.originalSelect.value=e.originalSelect.children[n.dataset.value].value}))}},{key:"_isValidNewSelectOption",value:function(e){return!(e.classList.contains("dropdown-select")||e.classList.contains("dd-searchbox")||"UL"===e.tagName||"SPAN"===e.tagName||e.classList.contains("list"))}},{key:"_addKeysListener",value:function(){var e=this;this.newSelect.addEventListener("keydown",(function(t){if(e.newSelect.classList.contains("open")){var n=t.target;13===t.keyCode?n.click():27===t.keyCode?e.newSelect.click():37===t.keyCode&&n.prevSibling?n.prevSibling.focus():40===t.keyCode&&n.nextSibling&&n.nextSibling.focus()}}))}},{key:"addOption",value:function(e){if(""!==e){e=e.toLowerCase();var t=document.createElement("option");t.value=e,t.innerHTML=e.capitalize(),t.selected=!0,this.originalSelect.appendChild(t),this._addItemToList(t,this.newSelect.children[1].children[1].childElementCount,!0)}}}])&&a(t.prototype,n),r&&a(t,r),e}()},18:function(e,t,n){e.exports=n(19)},19:function(e,t,n){"use strict";n.r(t),n.d(t,"setUpExportPractice",(function(){return a}));var i=n(0);function a(e){new i.a("id_filetype").createDropdown("Search for a format..."),document.getElementById("submit-export").addEventListener("click",(function(t){t.preventDefault(),fetch(new Request(e,{method:"POST",mode:"same-origin",headers:{"X-CSRFToken":main.getCsrfToken()},body:JSON.stringify({file_type:document.getElementById("id_filetype").value})})).then((function(){return toast({message:"We are exporting your practices. Please wait.",duration:3e3,type:"is-info",animate:{in:"fadeIn",out:"fadeOut"}})}))}))}n.d(t,"makeSearchableDropDown",(function(){return i.b}))}}));