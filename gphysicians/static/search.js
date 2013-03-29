
var KEY = 'AIzaSyDzvGIlo_6GmdRasOTnN17hJ9rS3hx_3OA';
var CX = '015533284649053097143:eyct-samxvy';

var state = null;

function parseParams() {
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

function renderResult(result) {
    return $('<li>')
        .append($('<h3>')
                .append($('<a>').attr('href', result.link).html(result.htmlTitle)))
        .append($('<cite>').html(result.formattedUrl))
        .append($('<p>').html(result.htmlSnippet.replace(/<br>/g, '')));
}

function renderSpelling(spelling) {
    var q = spelling.correctedQuery;
    return $('<div>').addClass('spelling')
        .append('Did you mean ')
        .append($('<a>').attr('href', searchUrl({q: q})).text(q)
                .on('click', function(e) {
                    state.q = q;
                    $('#query-text').val(q);
                    history.pushState(state, state.q, searchUrl(state));
                    search(state.q);
                    return false;
                }))
        .append('?');
}

function logQuery(query) {
    $.ajax({
        url: '/api/log',
        method: 'POST',
        data: {
            q: state.q
        }
    });
}

function searchUrl(state) {
    return location.pathname + '?' + $.param(state);
}

function search(query) {
    logQuery(query);
    var results = $('#results');
    $.ajax({
        url: 'https://www.googleapis.com/customsearch/v1',
        dataType: 'jsonp',
        data: {
            key: KEY,
            cx: CX,
            q: query
        },
        success: function(data) {
            results.empty();
            if (data.spelling)
                results.append(renderSpelling(data.spelling));

            if (data.items) {
                results.append($('<ol>').html($.map(data.items, renderResult)));
            } else {
                results.append(
                    $('<p>')
                        .append('No results for ')
                        .append($('<b>').text(data.queries.request[0].searchTerms)));
            }
        }
    });
}

$(document).ready(function() {
    $('#query-form').submit(function() {
        state.q = $('#query-text').val();
        history.pushState(state, state.q, searchUrl(state));
        search(state.q);
        return false;
    });
});

window.addEventListener('popstate', function(e) {
    state = e.state ? e.state : parseParams();
    $('#query-text').val(state.q);
    search(state.q);
});