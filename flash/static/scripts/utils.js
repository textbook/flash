lastUpdate = function(paneSelector) {
  var now = new Date();
  $(paneSelector + ' .last-update').text(
    'Last update: ' + now.toDateString() + ' ' + now.toLocaleTimeString()
  );
};