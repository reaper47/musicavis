!function(e,t){for(var n in t)e[n]=t[n]}(window,function(e){var t={};function n(i){if(t[i])return t[i].exports;var r=t[i]={i:i,l:!1,exports:{}};return e[i].call(r.exports,r,r.exports,n),r.l=!0,r.exports}return n.m=e,n.c=t,n.d=function(e,t,i){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:i})},n.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var i=Object.create(null);if(n.r(i),Object.defineProperty(i,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var r in e)n.d(i,r,function(t){return e[t]}.bind(null,r));return i},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="/static/assets/bundles/",n(n.s=146)}({1:function(e,t,n){"use strict";function i(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function r(e,t){for(var n=0;n<t.length;n++){var i=t[n];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(e,i.key,i)}}function a(e,t){var n=arguments.length>2&&void 0!==arguments[2]&&arguments[2],i=new s(e,n);return i.createDropdown(t),i}n.d(t,"b",(function(){return a})),n.d(t,"a",(function(){return s}));var s=function(){function e(t){var n=arguments.length>1&&void 0!==arguments[1]&&arguments[1];i(this,e),this.originalSelect=document.getElementById(t),this.options=Array.from(this.originalSelect.children),this.allowMultiple=n}var t,n,a;return t=e,(n=[{key:"createDropdown",value:function(e){var t=this,n=document.createElement("div");n.classList.add("dropdown-select","wide"),n.tabIndex=0;var i=document.createElement("span");i.classList.add("current"),i.textContent=this.options[0].textContent,n.appendChild(i);var r=document.createElement("div");r.classList.add("list");var a=document.createElement("div");a.classList.add("dd-search");var s=document.createElement("input");s.type="text",s.id="txtSearchValue",s.placeholder=e,s.classList.add("dd-searchbox"),s.autocomplete="off",s.onkeyup=function(){return t._filter()},this.searchBoxInput=s;var o=document.createElement("ul");this.searchBoxOptions=o,this._addItemsToList(this.options),a.appendChild(s),r.appendChild(a),r.appendChild(o),n.appendChild(r),this.newSelect=n,this.originalSelect.parentElement.appendChild(n),this.originalSelect.style.display="none",this._addOpenCloseListener(),this._addClickOutsideListener(),this._addOptionClickListener(),this._addKeysListener()}},{key:"_addItemsToList",value:function(e){var t=this;e.forEach((function(e,n){return t._addItemToList(e,n)})),this.allowMultiple||this.searchBoxOptions.firstElementChild.classList.add("selected")}},{key:"_addItemToList",value:function(e,t){var n=arguments.length>2&&void 0!==arguments[2]&&arguments[2],i=document.createElement("li");if(i.classList.add("option"),i.index,i.dataset.value=t,this.allowMultiple){var r=document.createElement("div");r.classList.add("multiple-select-item-container");var a=document.createElement("p");a.textContent=e.textContent,r.appendChild(a);var s=document.createElement("label"),o=document.createElement("input");s.classList.add("checkbox"),s.classList.add("checkbox-option"),o.classList.add("checkbox-option"),o.type="checkbox",n&&(i.classList.add("selected"),o.checked=!0),s.appendChild(o),r.append(s),i.appendChild(r)}else i.textContent=e.textContent;this.searchBoxOptions.appendChild(i)}},{key:"_filter",value:function(){var e=this;Array.from(this.searchBoxOptions.children).forEach((function(t){t.textContent.toLowerCase().includes(e.searchBoxInput.value)?t.style.display="block":t.style.display="none"}))}},{key:"_addOpenCloseListener",value:function(){var e=this;this.newSelect.addEventListener("click",(function(t){var n=t.target.classList,i=t.target.parentElement.classList;if(i.contains("open")||i.contains("multiple-select-item-container"))return e._removeTabIndex(),void(e.allowMultiple||e.newSelect.classList.remove("open"));n.contains("dd-searchbox")||n.contains("checkbox-option")||"UL"===t.target.tagName||(e.newSelect.classList.toggle("open"),Array.from(e.searchBoxOptions.children).forEach((function(e){return e.tabIndex=0})),e.searchBoxInput.focus())}))}},{key:"_addClickOutsideListener",value:function(){var e=this;document.addEventListener("click",(function(t){for(var n=t.target;"HTML"!==(n=n.parentElement).tagName;)if(Array.from(n.classList).includes("dropdown-select")&&e.allowMultiple)return;Array.from(t.target.classList).includes("dropdown-select")||(e.newSelect.classList.remove("open"),e.newSelect.removeAttribute("tabindex"),e._removeTabIndex()),t.stopPropagation()}))}},{key:"_removeTabIndex",value:function(){Array.from(this.searchBoxOptions.children).forEach((function(e){return e.removeAttribute("tabindex")}))}},{key:"_addOptionClickListener",value:function(){var e=this;this.newSelect.addEventListener("click",(function(t){var n=t.target;if(e._isValidNewSelectOption(n))if(e.allowMultiple){for(var i="INPUT"===n.tagName;"LI"!==n.tagName;)n=n.parentElement;var r=n.children[0].children[1].children[0];i||(r.checked^=1),r.checked?n.classList.add("selected"):n.classList.remove("selected"),e.originalSelect.children[n.dataset.value].selected=r.checked;var a=main.getSelectValues(e.originalSelect).join(", ");e.newSelect.firstChild.textContent=a||"None"}else Array.from(e.searchBoxOptions.children).forEach((function(e){return e.classList.remove("selected")})),n.classList.add("selected"),e.newSelect.firstChild.textContent=n.textContent,e.originalSelect.value=e.originalSelect.children[n.dataset.value].value}))}},{key:"_isValidNewSelectOption",value:function(e){return!(e.classList.contains("dropdown-select")||e.classList.contains("dd-searchbox")||"UL"===e.tagName||"SPAN"===e.tagName||e.classList.contains("list"))}},{key:"_addKeysListener",value:function(){var e=this;this.newSelect.addEventListener("keydown",(function(t){if(e.newSelect.classList.contains("open")){var n=t.target;13===t.keyCode?n.click():27===t.keyCode?e.newSelect.click():37===t.keyCode&&n.prevSibling?n.prevSibling.focus():40===t.keyCode&&n.nextSibling&&n.nextSibling.focus()}}))}},{key:"addOption",value:function(e){if(""!==e){e=e.toLowerCase();var t=document.createElement("option");t.value=e,t.innerHTML=e.capitalize(),t.selected=!0,this.originalSelect.appendChild(t),this._addItemToList(t,this.newSelect.children[1].children[1].childElementCount,!0)}}}])&&r(t.prototype,n),a&&r(t,a),e}()},146:function(e,t,n){e.exports=n(154)},154:function(e,t,n){"use strict";n.r(t);var i=n(1);function r(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function a(e,t){for(var n=0;n<t.length;n++){var i=t[n];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(e,i.key,i)}}function s(e,t,n){return t&&a(e.prototype,t),n&&a(e,n),e}var o=function(){function e(t,n,i){var a=arguments.length>3&&void 0!==arguments[3]?arguments[3]:null;r(this,e),this.workFunc=this._updateTimer,this.interval=n,this.errorFunc=a,this.timesUpFunc=i,this.timeComponents={hour:t.hour,minutes:t.minutes,seconds:t.seconds},this.sound=new Howl({src:"/sounds/sos.mp3",loop:!0})}return s(e,[{key:"start",value:function(e){this.time=e,this.originalTime=e,this.expected=Date.now()+this.interval,this.timeout=setTimeout(this.step.bind(this),this.interval),this.workFunc()}},{key:"stop",value:function(){clearTimeout(this.timeout),this._restoreTime(),this.sound.stop()}},{key:"step",value:function(){if(0==this.time)return this.sound.play(),void this.timesUpFunc();var e=Date.now()-this.expected;this.errorFunc&&e>this.interval&&this.errorFunc(),this.time--,this.workFunc(),this.expected+=this.interval,this.timeout=setTimeout(this.step.bind(this),Math.max(0,this.interval-e))}},{key:"_updateTimer",value:function(){var e=this._separateTime(this.time);this._updateTimeComponents(e)}},{key:"_restoreTime",value:function(){var e=this._separateTime(this.originalTime);this._updateTimeComponents(e)}},{key:"_separateTime",value:function(e){var t=Math.floor(e/3600),n=3600*t,i=Math.floor(Math.abs(n-e)/60);return{hours:t,minutes:i,seconds:e-n-60*i}}},{key:"_updateTimeComponents",value:function(e){this.timeComponents.hour.textContent=e.hours,this.timeComponents.minutes.textContent=e.minutes,this.timeComponents.seconds.textContent=e.seconds}}]),e}(),l=function(){function e(){var t=this;r(this,e),this._ctx=new AudioContext,this._soundBeatOne=new Howl({src:"/sounds/one.wav"}),this._soundBeatOther=new Howl({src:"/sounds/other.wav"}),this._soundBeatBetween=new Howl({src:"/sounds/between.wav"}),this._lastBar=0,this._lastBeat=0,this._metronome=window.MusicalTimer((function(){"running"!==t._ctx.state&&t._ctx.resume(),t._lastBar!==t._metronome.bar&&(t._lastBar=t._metronome.bar,t._beep(t._soundBeatOne)),t._lastBeat!==t._metronome.beat?(t._lastBeat=t._metronome.beat,t._beep(t._soundBeatBetween)):t._beep(t._soundBeatOther)}))}return s(e,[{key:"_beep",value:function(e){arguments.length>1&&void 0!==arguments[1]&&arguments[1];e.play();try{this._signatureVisual.children[this._metronome.beat-2].classList.remove("highlightBeat"),this._signatureVisual.children[this._metronome.beat-2].classList.remove("highlightBeat1"),this._signatureVisual.children[this._metronome.beat-1].classList.add("highlightBeat")}catch(e){this._signatureVisual.lastElementChild.classList.remove("highlightBeat"),this._signatureVisual.children[this._metronome.beat-1].classList.add("highlightBeat1")}this._barNumberElement.value=this._metronome.bar}},{key:"play",value:function(){this._metronome.play()}},{key:"pause",value:function(){this._metronome.pause()}},{key:"stop",value:function(){try{this._signatureVisual.children[this._metronome.beat-1].classList.remove("highlightBeat"),this._signatureVisual.children[this._metronome.beat-1].classList.remove("highlightBeat1")}finally{this._barNumberElement.value=1,this._metronome.stop()}}},{key:"setTempo",value:function(e){this._metronome.tempo=e}},{key:"setSignature",value:function(e){this._metronome.signature=e}},{key:"setSignatureVisual",value:function(e){this._signatureVisual=e}},{key:"setSubdivision",value:function(e){this._metronome.resolutionFactor=e}},{key:"setBarNumberElement",value:function(e){this._barNumberElement=e}}]),e}();function c(e){return function(e){if(Array.isArray(e)){for(var t=0,n=new Array(e.length);t<e.length;t++)n[t]=e[t];return n}}(e)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(e)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance")}()}function u(e,t){for(var n=0;n<t.length;n++){var i=t[n];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(e,i.key,i)}}n.d(t,"Practice",(function(){return d})),n.d(t,"makeSearchableDropDown",(function(){return i.b})),n.d(t,"SearchableDropdown",(function(){return i.a})),n.d(t,"Timer",(function(){return o})),n.d(t,"Metronome",(function(){return l}));var d=function(){function e(t){!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,e),this.lastActiveElement=null,this.practiceUrl=t,this.isDirty=!1}var t,n,i;return t=e,(n=[{key:"init",value:function(){var e=this;main.startTabsWithContent(),document.addEventListener("click",(function(){return e.__removeFocus(e.lastActiveElement)})),document.getElementById("submit-practice-form").addEventListener("click",(function(){return e.savePractice()})),document.getElementById("delete-practice-button").addEventListener("click",(function(){return e.deletePractice()})),Object.values(document.getElementsByClassName("add-row")).forEach((function(t){return e.__addNodeListener(t)})),Object.values(document.getElementsByClassName("remove-row")).forEach((function(t){return e.__removeNodeListener(t)})),Array.from(document.getElementsByClassName("change-listener")).forEach((function(t){return t.addEventListener("change",e.sessionKeysListener)})),document.addEventListener("keyup",(function(t){return e.sessionKeysListener(t)}))}},{key:"savePractice",value:function(){var e=this,t=!(arguments.length>0&&void 0!==arguments[0])||arguments[0];this.isDirty&&fetch(new Request(this.practiceUrl,{method:"POST",mode:"same-origin",body:new FormData(document.getElementById("practice-form"))})).then((function(e){return e.json()})).then((function(n){t&&toast({message:n.toast,type:"is-info",animate:{in:"fadeIn",out:"fadeOut"}}),e.isDirty=!1}))}},{key:"deletePractice",value:function(){confirm("Are you sure you want to delete this practice session?")&&fetch(new Request(this.practiceUrl,{method:"DELETE",mode:"same-origin",headers:{"X-CSRFToken":main.getCsrfToken()}})).then((function(e){return window.location.replace(e.url)}))}},{key:"sessionKeysListener",value:function(e){var t=e.altKey,n=e.code;if(this.isDirty=!0,t&&"KeyS"===n)this.savePractice();else if(t&&"Delete"===n)this.deletePractice();else if("Enter"===n){for(var i=e.srcElement;i=i.parentElement;)if(["UL","TABLE"].includes(i.tagName))return this.__addEntry(i)}else"Tab"===n&&this.__removeFocus(this.lastActiveElement)}},{key:"__addEntry",value:function(e){if("UL"===e.tagName){var t=e.lastElementChild.cloneNode(!0),n=t.children[1].children[0];this.__updateTextInput(n),e.appendChild(t)}else if("TABLE"===e.tagName){var i=e.tBodies[0].lastElementChild.cloneNode(!0);i.children[0].textContent="".concat(Number(i.children[0].textContent.split(".")[0])+1,"."),this.__updateTextInput(i.children[1].children[0]),this.__updateCellInput(i.children[2].children[0]),this.__updateCellInput(i.children[3].children[0]),this.__updateCellInput(i.children[4].children[0]),e.tBodies[0].appendChild(i)}}},{key:"__addNodeListener",value:function(e){var t=this;e.addEventListener("click",(function(e){for(var n=e.srcElement;"HEADER"!==n.tagName;)n=n.parentElement;"UL"!==(n=n.parentElement.children[1].children[0].children[0]).tagName&&(n=n.children[0]),t.__addEntry(n),t.isDirty=!0}))}},{key:"__removeNodeListener",value:function(e){var t=this;e.addEventListener("click",(function(e){var n=e.srcElement.parentElement.parentElement;["LI","TR"].includes(n.tagName)||(n=n.parentElement);var i=n.parentElement.children;if(1!==i.length){for(var r=c(n.parentNode.children).indexOf(n);r<i.length;r++){var a=i[r];"LI"===a.tagName&&(console.log(a,a.children[1].children[0].id),t.__updateTextInput(a.children[1].children[0],!0,!1))}n.parentElement.removeChild(n),t.isDirty=!0}else"LI"===n.tagName&&(n.children[1].children[0].value="")}))}},{key:"__updateTextInput",value:function(e){var t=arguments.length>1&&void 0!==arguments[1]&&arguments[1],n=!(arguments.length>2&&void 0!==arguments[2])||arguments[2],i=this.__createNewId(e.id,t);e.id=i,e.name=i,n&&(e.value="")}},{key:"__updateCellInput",value:function(e){var t=this.__createNewId(e.id);e.id=t,e.name=t,e.value=e.defaultValue,e.hasAttribute("min")||(e.value="")}},{key:"__createNewId",value:function(e){var t=arguments.length>1&&void 0!==arguments[1]&&arguments[1],n=e.split("_");return n[2]=t?Number(n[2])-1:Number(n[2])+1,n.join("_")}},{key:"__focusElement",value:function(e){e.focus(),e.className+=" is-focused"}},{key:"__removeFocus",value:function(e){e&&(e.classList.remove("is-focused"),e=null)}},{key:"exitConfirmation",value:function(){return this.isDirty?"There are unsaved changes. All your changes will be lost if you exit.":(this.isDirty=!1,null)}}])&&u(t.prototype,n),i&&u(t,i),e}()}}));