
function dropsort() {
    if ($("#server_comp").val() == 'new'){
        location.href = 'http://mimimimim.sakura.ne.jp/django.cgi/setting/server/create';
    }
    //get_id_pass();
    get_login();
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
    if (location.host == 'localhost:8000'){
      base_url = [location.protocol, '/', location.host, "id/pass.json"].join('/');
    } else {
      base_url = [location.protocol, '/', location.host, "django.cgi", "url_site.json"].join('/');
    }
    http_url = [base_url, $.param(query_params)].join('?');
    var xmlHttp;
    xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", http_url, false);
    xmlHttp.send(null);
    $('input[name=id]').val(JSON.parse(xmlHttp.responseText)["id"]);
    $('input[name=pass]').val(JSON.parse(xmlHttp.responseText)["pass"]);
}

function get_login(){
    url = $('select[name=company]').val();
    query_params = {
        'server': url
    };
    if (location.host == 'localhost:8000'){
      base_url = [location.protocol, '/', location.host, "get_login.json"].join('/');
    } else {
      base_url = [location.protocol, '/', location.host, "django.cgi", "get_login.json"].join('/');
    }
    http_url = [base_url, $.param(query_params)].join('?');
    var xmlHttp;
    xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", http_url, false);
    xmlHttp.send(null);
    $('input[name=login_url]').val(JSON.parse(xmlHttp.responseText)["login_url"]);
    $('input[name=login_id]').val(JSON.parse(xmlHttp.responseText)["login_id"]);
    $('input[name=login_pass]').val(JSON.parse(xmlHttp.responseText)["login_pass"]);
}

if (location.href == "http://localhost:8000/server/create"){
  get_login();
} else if (location.href == "http://mimimimim.sakura.ne.jp/django.cgi/server/create"){
  get_login();
}

function delete_check(site_id){
  if(confirm("本当に削除してもよいですか？")){
      console.log(location.host + "/site/delete?site_id=" + site_id);
      if (location.host == 'localhost:8000'){
        location.href = "http://" + location.host + "/site/delete?site_id=" + site_id;
      } else {
        location.href = "http://" + location.host + "django.cgi/site/delete?site_id=" + site_id;
      }
  }
}
