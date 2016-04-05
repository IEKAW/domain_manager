
function dropsort() {
    if ($("#server_comp").val() == 'new'){
        location.href = 'http://mimimimim.sakura.ne.jp/django.cgi/setting/server/create'
    }
    get_id_pass();
}

path = $(location).attr('pathname');
if (path == '/warning') {
    if (confirm("ドメインが登録されていません。続いてドメインの登録もしますか？")) {
    } else {
        location.href = '/django.cgi/site';
    }
}

// urlから自動でsite_titleを取得してくれる
function get_id_pass(){
    url = $('select[name=company]').val();
    query_params = {
        'server': url
    };
    //base_url = [location.protocol, '/', location.host, "id/pass.json"].join('/');
    base_url = [location.protocol, '/', location.host, "django.cgi", "url_site.json"].join('/');
    http_url = [base_url, $.param(query_params)].join('?');
    var xmlHttp;
    xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", http_url, false);
    xmlHttp.send(null);
    console.log(xmlHttp.responseText);
    $('input[name=id]').val(JSON.parse(xmlHttp.responseText)["id"]);
    $('input[name=pass]').val(JSON.parse(xmlHttp.responseText)["pass"]);
}

get_id_pass();