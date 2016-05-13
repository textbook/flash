/* globals $,$SERVICE_URL,SERVICES */

var setTileHealth = function(tile, health) {
  tile.removeClass('tile-ok tile-error');
  if (health === 'ok') {
    tile.addClass('tile-ok');
  } else if (health === 'error') {
    tile.addClass('tile-error');
  }
};

var updateCommit = function(element, data) {
  ['author', 'committed', 'message'].forEach(function (attr) {
    element.children('.' + attr).text(data[attr]);
  });
};

var updateItems = function(pane, items, selector, updater) {
  var elements = pane.children(selector);
  items.slice(0, 4).forEach(function (item, index) {
    updater(elements.eq(index), item);
  });
};

var updateOutcome = function(element, data) {
  element.removeClass('passed failed crashed cancelled working');
  element.addClass(data.outcome);
  ['author', 'elapsed', 'message', 'outcome'].forEach(function (attr) {
    element.children('.' + attr).text(data[attr]);
  });
};

var processPayload = function (payload) {
  for (var key in payload) {
    if (payload.hasOwnProperty(key)) {
      var data = payload[key];
      var tile = $('#' + key);
      var pane = tile.children('.pane').first();
      var serviceHandler = SERVICES[data.service_name];

      setTileHealth(tile, data.health || 'neutral');
      tile.find('.service-caption > .project-name').first().text(data.name);

      if (serviceHandler && data) {
        serviceHandler(pane, data);
      }
    }
  }
};

var updateServices = function() {
  $.getJSON($SERVICE_URL, function (payload) {
    if (payload) {
      console.info('received', payload);
      processPayload(payload);
    }
  });
};

/**
* bundleService puts tiles of the same kind into a wrapper element and animates the transition.
* bundleService as well as bundleServices could be nicely encapsulated in a jquery plugin.
*/
var bundleService = function (serviceSelector, interval) {
  console.log('bundle ', serviceSelector);
  var active = 0;
  var stacked = [];
  var wrapper = bundle(serviceSelector);

  function bundle(selector) {
    var tiles = $(selector).remove();
    var wrapper = $('<div class="tiles-stack"></div>');

    tiles.each(function (index, obj) {
      stacked[index] = $(obj);
      stacked[index].append('<div class="tiles-count">' + (index + 1) + ' of ' + tiles.length+ '</div>');
      wrapper.append(stacked[index]);
    });
    $('.dashboard').append(wrapper);

    return wrapper;
  }

  function updateStacked() {
    if (stacked.length === 0) return;
    var currentActive = active++ % stacked.length;
    wrapper.children().hide();

    stacked[currentActive]
      .show()
      .effect('shake', {distance: 10, times: 3});
  }

  updateStacked();
  setInterval(updateStacked, interval)
};

/**
* bundleServices goes over all tiles and finds tiles of the same kind > 1
* The order ot the tiles changes at the moment, tiles with more than one tile
* are appended to the end.
*/
function bundleServices() {
  var serviceTiles = $('.service-tile');
  var cssClassTotals = {}

  serviceTiles.each(function (index, obj) {
    $(obj).attr('class').match(/.*-tile/)[0].split(/\s+/).forEach(function (cssClass) {
      if (cssClass === 'service-tile') return;
      if (!cssClassTotals[cssClass]) cssClassTotals[cssClass] = 0;
      cssClassTotals[cssClass] += 1;
    })
  });

  for (var cssClass in cssClassTotals) {
    if (cssClassTotals.hasOwnProperty(cssClass)) {
      if (cssClassTotals[cssClass] > 1) {
        var cssSelector = '.' + cssClass;
        bundleService(cssSelector, 10000);
      }
    }
  }
}

$(document).ready(function () {
  bundleServices();
  updateServices();
  setInterval(updateServices, 60000);
});
