function lastUpdate (paneSelector) {
  var now = new Date();
  $(paneSelector + ' .last-update').text(
    'Last update: ' + now.toDateString() + ' ' + now.toLocaleTimeString()
  );
}

function elapsed (startTime, endTime) {
  var seconds = Math.round((new Date(endTime) - new Date(startTime)) / 1000);
  if (seconds === 1) {
    return '1 second';
  } else if (seconds < 60) {
    return seconds + ' seconds';
  } else if (seconds === 60) {
    return '1 minute';
  } else if (seconds < (60 * 60)) {
    return Math.round(seconds / 60) + ' minutes';
  } else if (seconds === (60 * 60)) {
    return '1 hour';
  } else if (seconds < (60 * 60 * 24)) {
    return Math.round(seconds / (60 * 60)) + ' hours';
  }
  return 'ages';
}

function truncate (text, maxLen) {
  if (text.length <= maxLen) {
    return text;
  }
  return text.slice(0, (maxLen - 3)) + '...';
}

function updateOutcome (element, data) {
  element.removeClass('success error');
  element.addClass(data.outcome);
  element.children('.message').text(truncate(data.message, 20));
  element.children('.elapsed').text('Took ' + elapsed(data.start, data.end));
  ['author', 'outcome'].forEach(function (attr) {
    element.children('.' + attr).text(data[attr]);
  });
}

function updateOutcomes(pane, builds) {
  var outcomes = pane.children('.build-outcome');
  builds.slice(0, 4).forEach(function (build, index) {
    updateOutcome(outcomes.eq(index), build);
  });
}
