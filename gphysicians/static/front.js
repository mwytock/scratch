
function renderRecentQueries(recent) {
    if (!recent) return null;
    
    var container = $('<div>');
    container.append($('<h2>').text('Recent queries'));
    var ul = $('<ul>');
    $.each(recent, function(i, e) {
        var q = e.query;
        ul.append($('<li>')
                  .append($('<a>').attr('href', '/search?' + $.param({q: q}))
                          .text(q)));
    });
    container.append(ul);
    return container;
}

$(document).ready(function() {
    $.ajax({
        url: '/api/recent',
        success: function(data) {
            $('#recent').html(renderRecentQueries(data.recent));
        },
    });
});