/*!
 * common js
 * By Jian Cao
 */


(function (doc) {
    var leftDoc = {
        init: function () {
            var titles_element = $('#article-content h3');
            if (titles_element) {
                var tpl = '<li><a href="#{{title}}">{{title}}</a></li>';
                var html = '';
                titles_element.each(function(index, data) {
                    var id = $(data).text();
                    $(data).attr('id', id);
                    html += tpl.replace(/{{title}}/g, id);
                });

                $('#navigation').html(html);
            }
        }
    };

    leftDoc.init();

})(document);
