// 全チェックの処理
$('#all').click(function(){
	$('input[name=record]').prop('checked', this.checked);
});

// checkedになっている項目岳削除する
function delete_data(kind){
    delete_ids = []
    $('[name=record]:checked').each(function(){
        delete_ids.push($(this).val());
    });
    console.log(delete_ids);
    for (var i = delete_ids.length - 1; i >= 0; i--) {
        query_params = {
            'kind': kind,
            'id': delete_ids[i]
        };
        base_url = [location.protocol, '/', location.host, 'delete_all'].join('/');
        url = [base_url, $.param(query_params)].join('?');
        communicate_http(url);
    };
    location.href="./unupdate";
}

function communicate_http(url){
    $.ajax({
          url: url,
          dataType: 'json',
          async: true,
          complete: function(data){
            var data_json = data.responseJSON;
            console.log(data_json);
            return data_json;
          }
    });
}
