
var KEY = 'AIzaSyDzvGIlo_6GmdRasOTnN17hJ9rS3hx_3OA';
var CX = '015533284649053097143:eyct-samxvy';

// The state of the page and the three UI components
var params = {};
var modes = null;
var query = null;
var results = null;

function parseLocation() {
    var params = {};
    if (!location.search) 
        return params;
    
    var vars = location.search.slice(1).split('&');
    for (var i=0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        var name = decodeURIComponent(pair[0]);
        var value = decodeURIComponent(pair[1]).replace(/\+/g, ' ');
        params[name] = value;
    }
    return params;
}

function title(params) {
    if (!params.q) return 'Stanford Medical Search';
    return params.q + ' - Stanford Medical Search';
}

function update(delta, replace) { 
    if (replace) 
        params = delta;
    else 
        for (k in delta) params[k] = delta[k];

    query.update(params);
    modes.update(params);
    results.update(params);
    document.title = title(params);
}

function pushHistory(params) {
    var url = location.pathname + '?' + $.param(params);
    history.pushState(params, title(params), url);
}

var ui = {};
ui.modes = function(root) {
    var selected = null;
    
    var el = {};
    el.update = function(params) {
        var mode = params.mode ? params.mode : 'web';
        var a = root.find('a[mode="' + mode + '"]');

        if (selected) selected.removeClass('selected');
        a.addClass('selected');
        selected = a;
    };

    root.find('a').on('click', function(e) {
        update({mode: $(this).attr('mode')});
        pushHistory(params);
    });
    
    return el;
};

ui.query = function(root) {
    var text = root.find('#query-text');

    var el = {};
    el.update = function(params) {
        if (!('q' in params)) return;
        text.val(params.q);
    };

    root.find('form').on('submit', function(e) {
        update({q: text.val()});
        pushHistory(params);
        return false;
    });

    return el;
};

ui.results = {};
ui.results.web = function(root) {
    var el = {};

    function result(data) {
        return $('<li>')
            .append($('<h3>')
                    .append($('<a>').attr('href', data.link)
                            .html(data.htmlTitle)))
            .append($('<cite>').html(data.formattedUrl))
            .append($('<p>').html(data.htmlSnippet.replace(/<br>/g, '')));
    }

    function spelling(data) {
        var q = data.correctedQuery;
        return $('<p>').addClass('spelling')
            .append('Did you mean ')
            .append($('<a>').text(q)
                    .on('click', function(e) {
                        update({q: q});
                        pushHistory(params);
                        return false;
                    }))
            .append('?');
    }
    
    function noResults(data) {
        return $('<p>')
            .append('No results for ')
            .append($('<b>').text(data.request[0].searchTerms));
    }

    el.update = function(params) {
        var query = params.q;
        if (params.mode == 'google') query += ' more:google';

        $.ajax({
            url: 'https://www.googleapis.com/customsearch/v1',
            dataType: 'jsonp',
            data: {
                key: KEY,
                cx: CX,
                q: query
            },
            success: function(data) {                
                root.empty();
                
                if (data.spelling)
                    root.append(spelling(data.spelling));
                
                if (data.items) {
                    root.append($('<ol>').addClass('web')
                                .html($.map(data.items, result)));
                } else {
                    root.append(noResults(data.queries));
                }
            }
        });
    };

    return el;

};

ui.results.images = function(root) {
    var el = {};

    function noResults(data) {
        return $('<p>')
            .append('No results for ')
            .append($('<b>').text(data.request[0].searchTerms));
    }

    function result(data) {
        var cite = data.image.width + ' &times; ' + data.image.height + ' - ' + 
            data.displayLink;
        console.log(data);
        return $('<li>')
            .append($('<a>')
                    .attr('href', data.image.contextLink)
                    .append($('<img>')
                            .attr('src', data.image.thumbnailLink))
                    .append($('<cite>').html(cite)));
    }

    function spelling(data) {
        var q = data.correctedQuery;
        return $('<p>').addClass('spelling')
            .append('Did you mean ')
            .append($('<a>').text(q)
                    .on('click', function(e) {
                        update({q: q});
                        pushHistory(params);
                        return false;
                    }))
            .append('?');
    }

    el.update = function(params) {
        $.ajax({
            url: 'https://www.googleapis.com/customsearch/v1',
            dataType: 'jsonp',
            data: {
                key: KEY,
                cx: CX,
                q: params.q,
                searchType: 'image',
                imgSize: 'medium'
            },
            success: function(data) {
                root.empty();

                if (data.spelling)
                    root.append(spelling(data.spelling));

                if (data.items) {
                    root.append($('<ol>').addClass('images')
                                .html($.map(data.items, result)));
                } else {
                    root.append(noResults(data.queries));
                }
            }
        });
    };

    return el;
};

ui.results.videos = function(root) {
    var el = {};
    el.update = function(params) {
        root.text('Coming soon');
    };
    return el;
};

ui.results.all = function(root) {
    var el = {};

    var web = ui.results.web(root);
    var results = {
        web: web,
        images: ui.results.images(root),
        videos: ui.results.videos(root),
        google: web
    }

    el.update = function(params) {
        log(params);
        results[params.mode ? params.mode : 'web'].update(params);
    };

    function log(params) {
        $.ajax({
            url: '/api/log',
            method: 'POST',
            data: params
        });
    }

    return el;
};

$(document).ready(function() {
    modes = ui.modes($('#modes'));
    query = ui.query($('#query'));
    results = ui.results.all($('#results'));
});

window.addEventListener('popstate', function(e) {
    update(e.state ? e.state : parseLocation(), true);
});

