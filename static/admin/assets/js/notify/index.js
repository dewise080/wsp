// Simple bootstrap-notify wrapper used by dashboard templates.
(function ($) {
  if (!$ || !$.notify) return;

  window.showDashboardNotification = function (message, type) {
    $.notify({ message: message || 'Notification' }, {
      type: type || 'primary',
      allow_dismiss: true,
      delay: 3000,
      placement: { from: 'top', align: 'right' },
    });
  };
})(window.jQuery);
