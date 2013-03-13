
var KEY = 'AIzaSyDzvGIlo_6GmdRasOTnN17hJ9rS3hx_3OA';
var CX = '015533284649053097143:eyct-samxvy';

function renderResult(result) {
    return $('<li>')
        .append($('<h3>')
                .append($('<a>').attr('href', result.link).html(result.htmlTitle)))
        .append($('<cite>').html(result.formattedUrl))
        .append($('<p>').html(result.htmlSnippet.replace(/<br>/g, '')));
}

function logQuery(query) {
    $.ajax({
        url: '/api/log',
        method: 'POST',
        data: {
            q: query
        }
    });
}

function search(query) {
    $.ajax({
        url: 'https://www.googleapis.com/customsearch/v1',
        dataType: 'jsonp',
        data: {
            key: KEY,
            cx: CX,
            q: query
        },
        success: function(data) {
            $('#results').html($('<ol>').html($.map(data.items, renderResult)));
        }
    });
}

$(document).ready(function() {
    $('#query-form').submit(function() {
        var q = $('#query-text').val();
        logQuery(q);
        search(q);
        return false;
    });
    search('diabetes');
});