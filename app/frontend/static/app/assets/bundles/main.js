!function(t,e){for(var n in e)t[n]=e[n]}(window,function(t){var e={};function n(i){if(e[i])return e[i].exports;var o=e[i]={i:i,l:!1,exports:{}};return t[i].call(o.exports,o,o.exports,n),o.l=!0,o.exports}return n.m=t,n.c=e,n.d=function(t,e,i){n.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:i})},n.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},n.t=function(t,e){if(1&e&&(t=n(t)),8&e)return t;if(4&e&&"object"==typeof t&&t&&t.__esModule)return t;var i=Object.create(null);if(n.r(i),Object.defineProperty(i,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var o in t)n.d(i,o,function(e){return t[e]}.bind(null,o));return i},n.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return n.d(e,"a",e),e},n.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},n.p="/static/assets/bundles/",n(n.s=133)}({133:function(t,e,n){t.exports=n(134)},134:function(t,e,n){"use strict";n.r(e);var i=n(5);n.d(e,"toast",(function(){return i.toast}));var o=n(3);n.d(e,"Main",(function(){return o.a})),n(135),String.prototype.capitalize=function(){return this.charAt(0).toUpperCase()+this.slice(1)}},135:function(t,e,n){"use strict";n.r(e);n(136),n(137),n(138),n(139),n(140),n(141),n(142);n(143),n(144)},136:function(t,e,n){},137:function(t,e,n){},138:function(t,e,n){},139:function(t,e,n){},140:function(t,e,n){},141:function(t,e,n){},142:function(t,e,n){},143:function(t,e,n){},144:function(t,e,n){},3:function(t,e,n){"use strict";var i=function(t){var e=t.documentElement,n=r(".modal"),i=r(".modal-button"),o=r(".modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button");function a(){e.classList.remove("is-clipped"),n.forEach((function(t){t.classList.remove("is-active")}))}function r(e){return Array.prototype.slice.call(t.querySelectorAll(e),0)}i.length>0&&i.forEach((function(n){n.addEventListener("click",(function(){var i=n.dataset.target,o=t.getElementById(i);e.classList.add("is-clipped"),o.classList.add("is-active")}))})),o.length>0&&o.forEach((function(t){t.addEventListener("click",(function(){a()}))})),t.addEventListener("keydown",(function(t){27===(t||window.event).keyCode&&a()}))};function o(t){return function(t){if(Array.isArray(t)){for(var e=0,n=new Array(t.length);e<t.length;e++)n[e]=t[e];return n}}(t)||function(t){if(Symbol.iterator in Object(t)||"[object Arguments]"===Object.prototype.toString.call(t))return Array.from(t)}(t)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance")}()}function a(t,e){for(var n=0;n<e.length;n++){var i=e[n];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(t,i.key,i)}}var r=function(){function t(e){!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,t),this.document=e,this.originalWindowTitle=e.title,this.cookieNotice(),i(e),this.initBurgers()}var e,n,r;return e=t,(n=[{key:"cookieNotice",value:function(){var t=this,e=this.document.getElementById("gdpr-notice");this.getCookie("gdpr")?e.style.display="none":(e.style.display="block",this.document.getElementById("gdpr-button").addEventListener("click",(function(){t.createCookie("gdpr",!0,31),e.classList.add("animated","bounceOutLeft")})))}},{key:"getCookie",value:function(t){return this.document.cookie.length>0&&this.document.cookie.split(";").map((function(t){return t.trim()})).find((function(e){return e.split("=")[0]===t}))}},{key:"createCookie",value:function(t,e,n){var i="";if(n){var o=new Date;o.setTime(o.getTime()+24*n*3600*1e3),i="; expires=".concat(o.toUTCString())}this.document.cookie="".concat(t,"=").concat(e).concat(i,"; path=/")}},{key:"create",value:function(t,e){var n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:null,i=this.document.createElement(t);return Object.keys(e).forEach((function(t){return i.setAttribute(t,e[t])})),null!=n&&n.appendChild(i),i}},{key:"submitFormOnEnter",value:function(t){this.document.addEventListener("keydown",(function(e){13===e.keyCode&&document.createElement("form").submit.call(t)}))}},{key:"removeElement",value:function(t){var e=this.document.getElementById(t);e.parentNode.removeChild(e)}},{key:"startTabsWithContent",value:function(){var t=this.document.querySelectorAll(".tabs li"),e=this.document.querySelectorAll(".tab-content"),n=function(t){return o(t.parentElement.children).indexOf(t)};t.forEach((function(i){i.addEventListener("click",(function(){t.forEach((function(t){return t.classList.remove("is-active")})),e.forEach((function(t){return t.classList.remove("is-active")})),i.classList.add("is-active"),function(t){e[n(t)].classList.add("is-active")}(i)}))})),t[0].click()}},{key:"isNumberKey",value:function(t){var e=t.which?t.which:event.keyCode;return!(e>31&&(e<48||e>57))}},{key:"getOtherElFromScreenType",value:function(t){return t.id.includes("mobile")?this.document.getElementById(t.id.split("-mobile")[0]):this.document.getElementById("".concat(t.id,"-mobile"))}},{key:"getSelectValues",value:function(t){return Array.from(t&&t.options).flatMap((function(t){return t.selected?[t.value||t.text]:[]}))}},{key:"getCsrfToken",value:function(){return document.querySelector("[name=csrfmiddlewaretoken]").value}},{key:"initBurgers",value:function(){Array.prototype.slice.call(document.querySelectorAll(".navbar-burger"),0).forEach((function(t){t.addEventListener("click",(function(){t.classList.toggle("is-active"),document.getElementById(t.dataset.target).classList.toggle("is-active")}))}))}},{key:"initNotifications",value:function(){var t=this;this.notificationsArea=document.getElementById("notifications"),document.addEventListener("mousedown",(function(e){for(var n=e.target;n&&!n.id.includes("notification-bell");){if(n.id.includes("notifications"))return void t.notificationsArea.classList.remove("hide");n=n.parentElement}n?t.notificationsArea.classList.toggle("hide"):t.notificationsArea.classList.add("hide")})),this.notificationsList=this.notificationsArea.lastElementChild.lastElementChild.firstElementChild,this.notificationBadge=document.getElementById("notification-badge"),this.noNotificationMessage=document.getElementById("no-notification")}},{key:"updateNotificationsList",value:function(t){var e=this,n=!(arguments.length>1&&void 0!==arguments[1])||arguments[1],i=JSON.parse(t),o=i.names.length;if(Number(this.notificationBadge.textContent)!==o){if(o>0){this.document.title="(".concat(o,") ").concat(this.originalWindowTitle),this._deleteNotifications(),this.notificationBadge.textContent=o,this.notificationBadge.classList.remove("hide"),this.noNotificationMessage.classList.add("hide");var a=this.document.createElement("ul");a.classList.add("notification-element"),i.names.forEach((function(t,n){var o=JSON.parse(i.data[n]);if(o.file_name&&t.includes("export_practice_task")){var r=e.document.createElement("li");r.classList.add("dropdown-item");var s=e.document.createElement("a");s.textContent="Your ".concat(o.file_name.split(".")[1].toUpperCase()," file is ready. Click here to download it"),s.href="/exports/".concat(o.file_name),s.setAttribute("download",""),r.appendChild(s),a.appendChild(r),e.notificationsList.appendChild(a)}}))}else this.document.title=this.originalWindowTitle,this._deleteNotifications(),this.notificationBadge.textContent=0,this.notificationBadge.classList.add("hide"),this.noNotificationMessage.classList.remove("hide");n&&this.notificationsArea.classList.add("hide")}}},{key:"_deleteNotifications",value:function(){Array.from(this.document.getElementsByClassName("notification-element")).forEach((function(t){return t.parentElement.removeChild(t)}))}}])&&a(e.prototype,n),r&&a(e,r),t}();e.a=r},5:function(t,e,n){
/*!
 * bulma-toast 1.5.4 
 * (c) 2018-present @rfoel <rafaelfr@outlook.com> 
 * Released under the MIT License.
 */
!function(t){"use strict";function e(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}function n(t,e){for(var n,i=0;i<e.length;i++)(n=e[i]).enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(t,n.key,n)}function i(t,e,i){return e&&n(t.prototype,e),i&&n(t,i),t}function o(){for(var t in(s={noticesTopLeft:l.createElement("div"),noticesTopRight:l.createElement("div"),noticesBottomLeft:l.createElement("div"),noticesBottomRight:l.createElement("div"),noticesTopCenter:l.createElement("div"),noticesBottomCenter:l.createElement("div"),noticesCenter:l.createElement("div")}).noticesTopLeft.setAttribute("style","".concat("width:100%;z-index:99999;position:fixed;pointer-events:none;display:flex;flex-direction:column;padding:15px;","left:0;top:0;text-align:left;align-items:flex-start;")),s.noticesTopRight.setAttribute("style","".concat("width:100%;z-index:99999;position:fixed;pointer-events:none;display:flex;flex-direction:column;padding:15px;","right:0;top:0;text-align:right;align-items:flex-end;")),s.noticesBottomLeft.setAttribute("style","".concat("width:100%;z-index:99999;position:fixed;pointer-events:none;display:flex;flex-direction:column;padding:15px;","left:0;bottom:0;text-align:left;align-items:flex-start;")),s.noticesBottomRight.setAttribute("style","".concat("width:100%;z-index:99999;position:fixed;pointer-events:none;display:flex;flex-direction:column;padding:15px;","right:0;bottom:0;text-align:right;align-items:flex-end;")),s.noticesTopCenter.setAttribute("style","".concat("width:100%;z-index:99999;position:fixed;pointer-events:none;display:flex;flex-direction:column;padding:15px;","top:0;left:0;right:0;text-align:center;align-items:center;")),s.noticesBottomCenter.setAttribute("style","".concat("width:100%;z-index:99999;position:fixed;pointer-events:none;display:flex;flex-direction:column;padding:15px;","bottom:0;left:0;right:0;text-align:center;align-items:center;")),s.noticesCenter.setAttribute("style","".concat("width:100%;z-index:99999;position:fixed;pointer-events:none;display:flex;flex-direction:column;padding:15px;","top:0;left:0;right:0;bottom:0;flex-flow:column;justify-content:center;align-items:center;")),s)l.body.appendChild(s[t]);c={"top-left":s.noticesTopLeft,"top-right":s.noticesTopRight,"top-center":s.noticesTopCenter,"bottom-left":s.noticesBottomLeft,"bottom-right":s.noticesBottomRight,"bottom-center":s.noticesBottomCenter,center:s.noticesCenter},r=!0}var a={message:"Your message here",duration:2e3,position:"top-right",closeOnClick:!0,opacity:1},r=!1,s={},c={},l=document,d=function(){function t(n){var i=this;e(this,t),this.element=l.createElement("div"),this.opacity=n.opacity,this.type=n.type,this.animate=n.animate,this.dismissible=n.dismissible,this.closeOnClick=n.closeOnClick,this.message=n.message,this.duration=n.duration,this.pauseOnHover=n.pauseOnHover;var o="width:auto;pointer-events:auto;display:inline-flex;white-space:pre-wrap;opacity:".concat(this.opacity,";"),a=["notification"];if(this.type&&a.push(this.type),this.animate&&this.animate.in&&(a.push("animated ".concat(this.animate.in)),this.onAnimationEnd((function(){return i.element.classList.remove(i.animate.in)}))),this.element.className=a.join(" "),this.dismissible){var r=l.createElement("button");r.className="delete",r.addEventListener("click",(function(){i.destroy()})),this.element.insertAdjacentElement("afterbegin",r)}else o+="padding: 1.25rem 1.5rem";this.closeOnClick&&this.element.addEventListener("click",(function(){i.destroy()})),this.element.setAttribute("style",o),"string"==typeof this.message?this.element.insertAdjacentHTML("beforeend",this.message):this.element.appendChild(this.message);var s=new u((function(){i.destroy()}),this.duration);this.pauseOnHover&&(this.element.addEventListener("mouseover",(function(){s.pause()})),this.element.addEventListener("mouseout",(function(){s.resume()})))}return i(t,[{key:"destroy",value:function(){var t=this;this.animate&&this.animate.out?(this.element.classList.add(this.animate.out),this.onAnimationEnd((function(){return t.removeChild(t.element)}))):this.removeChild(this.element)}},{key:"removeChild",value:function(t){t.parentNode&&t.parentNode.removeChild(t)}},{key:"onAnimationEnd",value:function(){var t=0<arguments.length&&void 0!==arguments[0]?arguments[0]:function(){},e={animation:"animationend",OAnimation:"oAnimationEnd",MozAnimation:"mozAnimationEnd",WebkitAnimation:"webkitAnimationEnd"};for(var n in e)if(void 0!==this.element.style[n]){this.element.addEventListener(e[n],(function(){return t()}));break}}}]),t}(),u=function(){function t(n,i){e(this,t),this.timer,this.start,this.remaining=i,this.callback=n,this.resume()}return i(t,[{key:"pause",value:function(){window.clearTimeout(this.timer),this.remaining-=new Date-this.start}},{key:"resume",value:function(){this.start=new Date,window.clearTimeout(this.timer),this.timer=window.setTimeout(this.callback,this.remaining)}}]),t}();t.setDoc=function(t){for(var e in s){var n=s[e];n.parentNode.removeChild(n)}l=t,o()},t.toast=function(t){r||o();var e=Object.assign({},a,t),n=new d(e);(c[e.position]||c[a.position]).appendChild(n.element)},Object.defineProperty(t,"__esModule",{value:!0})}(e)}}));