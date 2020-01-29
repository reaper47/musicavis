!function(e,t){for(var n in t)e[n]=t[n]}(window,function(e){var t={};function n(i){if(t[i])return t[i].exports;var o=t[i]={i:i,l:!1,exports:{}};return e[i].call(o.exports,o,o.exports,n),o.l=!0,o.exports}return n.m=e,n.c=t,n.d=function(e,t,i){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:i})},n.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var i=Object.create(null);if(n.r(i),Object.defineProperty(i,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var o in e)n.d(i,o,function(t){return e[t]}.bind(null,o));return i},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="/static/assets/bundles/",n(n.s=144)}({1:function(e,t,n){"use strict";function i(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function o(e,t){for(var n=0;n<t.length;n++){var i=t[n];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(e,i.key,i)}}function a(e,t){var n=arguments.length>2&&void 0!==arguments[2]&&arguments[2],i=new r(e,n);return i.createDropdown(t),i}n.d(t,"b",(function(){return a})),n.d(t,"a",(function(){return r}));var r=function(){function e(t){var n=arguments.length>1&&void 0!==arguments[1]&&arguments[1];i(this,e),this.originalSelect=document.getElementById(t),this.options=Array.from(this.originalSelect.children),this.allowMultiple=n}var t,n,a;return t=e,(n=[{key:"createDropdown",value:function(e){var t=this,n=document.createElement("div");n.classList.add("dropdown-select","wide"),n.tabIndex=0;var i=document.createElement("span");i.classList.add("current"),i.textContent=this.options[0].textContent,n.appendChild(i);var o=document.createElement("div");o.classList.add("list");var a=document.createElement("div");a.classList.add("dd-search");var r=document.createElement("input");r.type="text",r.id="txtSearchValue",r.placeholder=e,r.classList.add("dd-searchbox"),r.autocomplete="off",r.onkeyup=function(){return t._filter()},this.searchBoxInput=r;var c=document.createElement("ul");this.searchBoxOptions=c,this._addItemsToList(this.options),a.appendChild(r),o.appendChild(a),o.appendChild(c),n.appendChild(o),this.newSelect=n,this.originalSelect.parentElement.appendChild(n),this.originalSelect.style.display="none",this._addOpenCloseListener(),this._addClickOutsideListener(),this._addOptionClickListener(),this._addKeysListener()}},{key:"_addItemsToList",value:function(e){var t=this;e.forEach((function(e,n){return t._addItemToList(e,n)})),this.allowMultiple||this.searchBoxOptions.firstElementChild.classList.add("selected")}},{key:"_addItemToList",value:function(e,t){var n=arguments.length>2&&void 0!==arguments[2]&&arguments[2],i=document.createElement("li");if(i.classList.add("option"),i.index,i.dataset.value=t,this.allowMultiple){var o=document.createElement("div");o.classList.add("multiple-select-item-container");var a=document.createElement("p");a.textContent=e.textContent,o.appendChild(a);var r=document.createElement("label"),c=document.createElement("input");r.classList.add("checkbox"),r.classList.add("checkbox-option"),c.classList.add("checkbox-option"),c.type="checkbox",n&&(i.classList.add("selected"),c.checked=!0),r.appendChild(c),o.append(r),i.appendChild(o)}else i.textContent=e.textContent;this.searchBoxOptions.appendChild(i)}},{key:"_filter",value:function(){var e=this;Array.from(this.searchBoxOptions.children).forEach((function(t){t.textContent.toLowerCase().includes(e.searchBoxInput.value)?t.style.display="block":t.style.display="none"}))}},{key:"_addOpenCloseListener",value:function(){var e=this;this.newSelect.addEventListener("click",(function(t){var n=t.target.classList,i=t.target.parentElement.classList;if(i.contains("open")||i.contains("multiple-select-item-container"))return e._removeTabIndex(),void(e.allowMultiple||e.newSelect.classList.remove("open"));n.contains("dd-searchbox")||n.contains("checkbox-option")||"UL"===t.target.tagName||(e.newSelect.classList.toggle("open"),Array.from(e.searchBoxOptions.children).forEach((function(e){return e.tabIndex=0})),e.searchBoxInput.focus())}))}},{key:"_addClickOutsideListener",value:function(){var e=this;document.addEventListener("click",(function(t){for(var n=t.target;"HTML"!==(n=n.parentElement).tagName;)if(Array.from(n.classList).includes("dropdown-select")&&e.allowMultiple)return;Array.from(t.target.classList).includes("dropdown-select")||(e.newSelect.classList.remove("open"),e.newSelect.removeAttribute("tabindex"),e._removeTabIndex()),t.stopPropagation()}))}},{key:"_removeTabIndex",value:function(){Array.from(this.searchBoxOptions.children).forEach((function(e){return e.removeAttribute("tabindex")}))}},{key:"_addOptionClickListener",value:function(){var e=this;this.newSelect.addEventListener("click",(function(t){var n=t.target;if(e._isValidNewSelectOption(n))if(e.allowMultiple){for(var i="INPUT"===n.tagName;"LI"!==n.tagName;)n=n.parentElement;var o=n.children[0].children[1].children[0];i||(o.checked^=1),o.checked?n.classList.add("selected"):n.classList.remove("selected"),e.originalSelect.children[n.dataset.value].selected=o.checked;var a=main.getSelectValues(e.originalSelect).join(", ");e.newSelect.firstChild.textContent=a||"None"}else Array.from(e.searchBoxOptions.children).forEach((function(e){return e.classList.remove("selected")})),n.classList.add("selected"),e.newSelect.firstChild.textContent=n.textContent,e.originalSelect.value=e.originalSelect.children[n.dataset.value].value}))}},{key:"_isValidNewSelectOption",value:function(e){return!(e.classList.contains("dropdown-select")||e.classList.contains("dd-searchbox")||"UL"===e.tagName||"SPAN"===e.tagName||e.classList.contains("list"))}},{key:"_addKeysListener",value:function(){var e=this;this.newSelect.addEventListener("keydown",(function(t){if(e.newSelect.classList.contains("open")){var n=t.target;13===t.keyCode?n.click():27===t.keyCode?e.newSelect.click():37===t.keyCode&&n.prevSibling?n.prevSibling.focus():40===t.keyCode&&n.nextSibling&&n.nextSibling.focus()}}))}},{key:"addOption",value:function(e){if(""!==e){e=e.toLowerCase();var t=document.createElement("option");t.value=e,t.innerHTML=e.capitalize(),t.selected=!0,this.originalSelect.appendChild(t),this._addItemToList(t,this.newSelect.children[1].children[1].childElementCount,!0)}}}])&&o(t.prototype,n),a&&o(t,a),e}()},144:function(e,t,n){e.exports=n(145)},145:function(e,t,n){"use strict";n.r(t),n.d(t,"pushNewInstrument",(function(){return o})),n.d(t,"settingsPracticeLoad",(function(){return a}));var i=n(1);n.d(t,"makeSearchableDropDown",(function(){return i.b})),n.d(t,"SearchableDropdown",(function(){return i.a}));n(2);function o(e,t,n,i){var o=e.value;""!==o?(t.classList.add("hide"),e.classList.add("hide"),e.value="",n.classList.remove("hide"),fetch(new Request("/add-new-instrument/",{method:"POST",mode:"same-origin",headers:{"X-CSRFToken":main.getCsrfToken()},body:JSON.stringify({name:o})})).then((function(){return i.addOption(o)}))):e.focus()}function a(){var e=Object(i.b)("id_instruments","Search for an instrument...",!0),t=document.getElementById("confirm-add-instrument"),n=document.getElementById("add-instrument"),a=document.getElementById("new-instrument");a.addEventListener("keydown",(function(i){"Enter"===i.code&&(i.preventDefault(),o(a,t,n,e))})),n.addEventListener("click",(function(){t.classList.remove("hide"),n.classList.add("hide"),a.classList.remove("hide"),a.focus()})),t.addEventListener("click",(function(){return o(a,t,n,e)}))}},2:function(e,t,n){"use strict";var i=function(e){var t=e.documentElement,n=r(".modal"),i=r(".modal-button"),o=r(".modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button");function a(){t.classList.remove("is-clipped"),n.forEach((function(e){e.classList.remove("is-active")}))}function r(t){return Array.prototype.slice.call(e.querySelectorAll(t),0)}i.length>0&&i.forEach((function(n){n.addEventListener("click",(function(){var i=n.dataset.target,o=e.getElementById(i);t.classList.add("is-clipped"),o.classList.add("is-active")}))})),o.length>0&&o.forEach((function(e){e.addEventListener("click",(function(){a()}))})),e.addEventListener("keydown",(function(e){27===(e||window.event).keyCode&&a()}))};function o(e){return function(e){if(Array.isArray(e)){for(var t=0,n=new Array(e.length);t<e.length;t++)n[t]=e[t];return n}}(e)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(e)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance")}()}function a(e,t){for(var n=0;n<t.length;n++){var i=t[n];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(e,i.key,i)}}var r=function(){function e(t){!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,e),this.document=t,this.originalWindowTitle=t.title,this.cookieNotice(),i(t),this.initBurgers()}var t,n,r;return t=e,(n=[{key:"cookieNotice",value:function(){var e=this,t=this.document.getElementById("gdpr-notice");this.getCookie("gdpr")?t.style.display="none":(t.style.display="block",this.document.getElementById("gdpr-button").addEventListener("click",(function(){e.createCookie("gdpr",!0,31),t.classList.add("animated","bounceOutLeft")})))}},{key:"getCookie",value:function(e){return this.document.cookie.length>0&&this.document.cookie.split(";").map((function(e){return e.trim()})).find((function(t){return t.split("=")[0]===e}))}},{key:"createCookie",value:function(e,t,n){var i="";if(n){var o=new Date;o.setTime(o.getTime()+24*n*3600*1e3),i="; expires=".concat(o.toUTCString())}this.document.cookie="".concat(e,"=").concat(t).concat(i,"; path=/")}},{key:"create",value:function(e,t){var n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:null,i=this.document.createElement(e);return Object.keys(t).forEach((function(e){return i.setAttribute(e,t[e])})),null!=n&&n.appendChild(i),i}},{key:"submitFormOnEnter",value:function(e){this.document.addEventListener("keydown",(function(t){13===t.keyCode&&document.createElement("form").submit.call(e)}))}},{key:"removeElement",value:function(e){var t=this.document.getElementById(e);t.parentNode.removeChild(t)}},{key:"startTabsWithContent",value:function(){var e=this.document.querySelectorAll(".tabs li"),t=this.document.querySelectorAll(".tab-content"),n=function(e){return o(e.parentElement.children).indexOf(e)};e.forEach((function(i){i.addEventListener("click",(function(){e.forEach((function(e){return e.classList.remove("is-active")})),t.forEach((function(e){return e.classList.remove("is-active")})),i.classList.add("is-active"),function(e){t[n(e)].classList.add("is-active")}(i)}))})),e[0].click()}},{key:"isNumberKey",value:function(e){var t=e.which?e.which:event.keyCode;return!(t>31&&(t<48||t>57))}},{key:"getOtherElFromScreenType",value:function(e){return e.id.includes("mobile")?this.document.getElementById(e.id.split("-mobile")[0]):this.document.getElementById("".concat(e.id,"-mobile"))}},{key:"getSelectValues",value:function(e){return Array.from(e&&e.options).flatMap((function(e){return e.selected?[e.value||e.text]:[]}))}},{key:"getCsrfToken",value:function(){return document.querySelector("[name=csrfmiddlewaretoken]").value}},{key:"initBurgers",value:function(){Array.prototype.slice.call(document.querySelectorAll(".navbar-burger"),0).forEach((function(e){e.addEventListener("click",(function(){e.classList.toggle("is-active"),document.getElementById(e.dataset.target).classList.toggle("is-active")}))}))}},{key:"initNotifications",value:function(){var e=this;this.notificationsArea=document.getElementById("notifications"),document.addEventListener("mousedown",(function(t){for(var n=t.target;n&&!n.id.includes("notification-bell");){if(n.id.includes("notifications"))return void e.notificationsArea.classList.remove("hide");n=n.parentElement}n?e.notificationsArea.classList.toggle("hide"):e.notificationsArea.classList.add("hide")})),this.notificationsList=this.notificationsArea.lastElementChild.lastElementChild.firstElementChild,this.notificationBadge=document.getElementById("notification-badge"),this.noNotificationMessage=document.getElementById("no-notification")}},{key:"updateNotificationsList",value:function(e){var t=this,n=!(arguments.length>1&&void 0!==arguments[1])||arguments[1],i=JSON.parse(e),o=i.names.length;if(Number(this.notificationBadge.textContent)!==o){if(o>0){this.document.title="(".concat(o,") ").concat(this.originalWindowTitle),this._deleteNotifications(),this.notificationBadge.textContent=o,this.notificationBadge.classList.remove("hide"),this.noNotificationMessage.classList.add("hide");var a=this.document.createElement("ul");a.classList.add("notification-element"),i.names.forEach((function(e,n){var o=JSON.parse(i.data[n]);if(o.file_name&&e.includes("export_practice_task")){var r=t.document.createElement("li");r.classList.add("dropdown-item");var c=t.document.createElement("a");c.textContent="Your ".concat(o.file_name.split(".")[1].toUpperCase()," file is ready. Click here to download it"),c.href="/exports/".concat(o.file_name),c.setAttribute("download",""),r.appendChild(c),a.appendChild(r),t.notificationsList.appendChild(a)}}))}else this.document.title=this.originalWindowTitle,this._deleteNotifications(),this.notificationBadge.textContent=0,this.notificationBadge.classList.add("hide"),this.noNotificationMessage.classList.remove("hide");n&&this.notificationsArea.classList.add("hide")}}},{key:"_deleteNotifications",value:function(){Array.from(this.document.getElementsByClassName("notification-element")).forEach((function(e){return e.parentElement.removeChild(e)}))}}])&&a(t.prototype,n),r&&a(t,r),e}();t.a=r}}));