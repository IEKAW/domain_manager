/*
check項目を削除するスクリプト
 */

// 全チェックの処理
$('#all').click(function(){
	$('input[name=record]').prop('checked', this.checked);
});

// checkedになっている項目岳削除する
function delete_data(kind, id){
    delete_ids = [];
    if (id == null) {
        $('[name=record]:checked').each(function () {
            delete_ids.push($(this).val());
        });
    } else {
        delete_ids.push(id);
    }
    console.log(delete_ids);
    for (var i = delete_ids.length - 1; i >= 0; i--) {
        query_params = {
            'kind': kind,
            'id': delete_ids[i]
        };
        if (location.host == 'mimimimim.sakura.ne.jp') {
            base_url = [location.protocol, '/', location.host, 'django.cgi', 'delete_all'].join('/');
        } else {
            base_url = [location.protocol, '/', location.host, 'delete_all'].join('/');
        };
        url = [base_url, $.param(query_params)].join('?');
        communicate_http(url);
    };
    if (kind == 'domain' || kind == 'server') {
        location.href = "./unupdate";
    } else {
        console.log("aaa");
    }
}


// urlから自動でsite_titleを取得してくれる
function get_site(){
    url = $('select[name=link_url]').val();
    query_params = {
        'url': url
    };
    id = $('select[name=link_url] option:selected').attr('id');
    base_url = [location.protocol, '/', location.host, "django.cgi", "url_site.json"].join('/');
    // base_url = [location.protocol, '/', location.host, "django.cgi", "url_site.json"].join('/');
    http_url = [base_url, $.param(query_params)].join('?');
    var xmlHttp;
    xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", http_url, false);
    xmlHttp.send(null);
    $('input[name=link_site]').val(JSON.parse(xmlHttp.responseText)["site"][id]);
}


// urlから自動でsite_titleを取得してくれる
function get_url(){
    site = $('select[name=link_site]').val();
    query_params = {
        'site': site
    };
    id = $('select[name=link_site] option:selected').attr('id');
    base_url = [location.protocol, '/', location.host,"django.cgi" ,"site_url.json"].join('/');
    // base_url = [location.protocol, '/', location.host, "django.cgi", "url_site.json"].join('/');
    http_url = [base_url, $.param(query_params)].join('?');
    var xmlHttp;
    xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", http_url, false);
    xmlHttp.send(null);
    $('input[name=link_url]').val(JSON.parse(xmlHttp.responseText)["url"][0]);
}


// urlから自動でsite_titleを取得してくれる
function get_urls(){
    site = $('select[name=site_title]').val();
    query_params = {
        'site': site
    };
    id = $('select[name=site_title] option:selected').attr('id');
    base_url = [location.protocol, '/', location.host, "django.cgi" ,"site_url.json"].join('/');
    // base_url = [location.protocol, '/', location.host, "django.cgi", "url_site.json"].join('/');
    http_url = [base_url, $.param(query_params)].join('?');
    var xmlHttp;
    xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", http_url, false);
    xmlHttp.send(null);
    $('input[name=url]').val(JSON.parse(xmlHttp.responseText)["url"][0]);
}

function communicate_http(url){
    // $.ajax({
    //       url: url,
    //       dataType: 'json',
    //       async: true,
    //       complete: function(data){
    //         var data_json = data.responseJSON;
    //         console.log(data_json);
    //         return data_json;
    //       }
    // });
    var xmlHttp;
    xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", url, false);
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

function delete_confirm(check_id) {
    path = $(location).attr('pathname').split('/')[1];
    if (path == 'setting') {
        query_params = {
            'check_id': check_id,
            'kind': $(location).attr('pathname').split('/')[2]
        }
        base_url = [location.protocol, '/', location.host, "django.cgi" ,"delete_confirm.json"].join('/');
        http_url = [base_url, $.param(query_params)].join('?');
        var xmlHttp;
        xmlHttp = new XMLHttpRequest();
        xmlHttp.open("GET", http_url, false);
        xmlHttp.send(null);
        if (JSON.parse(xmlHttp.responseText)["result"] == 'yes'){
            $('a#' + check_id).attr('href', "/setting/" + $(location).attr('pathname').split('/')[2]);
            alert("この項目を使用している" + JSON.parse(xmlHttp.responseText)["reason"][0] + "がある為、削除が出来ません");
        }
    }
}

