'use strict';

function initModals(document) {
    const rootEl = document.documentElement;
    const $modals = getAll('.modal');
    const $modalButtons = getAll('.modal-button');
    const $modalCloses = getAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button');

    if ($modalButtons.length > 0) {
      $modalButtons.forEach(($el) => {
        $el.addEventListener('click', () => {
          const target = $el.dataset.target;
          const $target = document.getElementById(target);
          rootEl.classList.add('is-clipped');
          $target.classList.add('is-active');
        });
      });
    }

    if ($modalCloses.length > 0) {
      $modalCloses.forEach(($el) => {
        $el.addEventListener('click', function () {
          closeModals();
        });
      });
    }

    document.addEventListener('keydown', (event) => {
      var e = event || window.event;
      if (e.keyCode === 27) {
        closeModals();
      }
    });

    function closeModals() {
      rootEl.classList.remove('is-clipped');
      $modals.forEach(($el) => {
        $el.classList.remove('is-active');
      });
    }

    function getAll(selector) {
      return Array.prototype.slice.call(document.querySelectorAll(selector), 0);
    }
}

export default initModals;
