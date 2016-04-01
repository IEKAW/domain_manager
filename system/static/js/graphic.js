function dropsort() {
    if ($("#server_comp").val() == 'new'){
        location.href = 'http://mimimimim.sakura.ne.jp/django.cgi/setting/server/create'
    }
}

path = $(location).attr('pathname');
if (path == '/warning') {
    if (confirm("ドメインが登録されていません。続いてドメインの登録もしますか？")) {
    } else {
        location.href = '/django.cgi/site';
    }
}