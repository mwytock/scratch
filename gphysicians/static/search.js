
function logQuery(query) {
    $.ajax({
        url: '/api/log',
        method: 'POST',
        data: {
            q: query
        }
    });
}

function loaded() {
    // Log the initial query
    if (location.search.slice(3)) logQuery(
        decodeURIComponent(location.search.slice(3)).replace(/\+/g, ' '));

    // Log queries on either return or click on search button
    var input = $('input.gsc-input');
    $('input.gsc-search-button').click(function() { logQuery(input.val()); });
    $(input).keydown(function(e) { 
        if (e.keyCode == 13) logQuery(input.val()); 
    });
}