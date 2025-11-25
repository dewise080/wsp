(function ($) {
  'use strict';
  if (!$ || !$.fn.typeahead) return;

  var sampleData = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.whitespace,
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    local: ['Dashboard', 'Users', 'Settings', 'Reports', 'Logout'],
  });

  $('.Typeahead-input').typeahead({
    hint: true,
    highlight: true,
    minLength: 1,
  }, {
    name: 'sampleData',
    source: sampleData,
  });
})(window.jQuery);
