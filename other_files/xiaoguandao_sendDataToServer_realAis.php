<?php
  // 时间: 2022-10-26
  // 作者: DJW
  // 功能: 小管岛将数采和ais历史数据传到云端

  // 跨域解决
  header("Content-type:text/json;charset=UTF-8");
  // header("Access-Control-Allow-Origin:*");
  // 连接数据库
  $conn = new mysqli("127.0.0.1", "zz", "zzZZ4144670..", "shandong_db") or die("连接失败!");
  mysqli_query($conn, "set character set 'utf8'");
  mysqli_set_charset($conn, 'utf8');
  // var_dump($conn);
  // 获取json数据
  $input = file_get_contents("php://input");
  $input_json = json_decode($input);
  
  $id = $input_json->id;
  $times = $input_json->times;
  $mmsi = $input_json->mmsi; 
  $shipname = $input_json->shipname; 
  $lon = $input_json->lon; 
  $lat = $input_json->lat; 
  $speed = $input_json->speed; 
  $course = $input_json->course; 
  $heading = $input_json->heading; 
  $status = $input_json->status; 
  $callsign = $input_json->callsign; 
  $destination = $input_json->destination; 
  $shiptype = $input_json->shiptype; 
  $distance = $input_json->distance;   


  $sql = "INSERT IGNORE INTO `xiaoguandao_ais_tbl`(id,times,mmsi) VALUES($id,'$times','$mmsi');";
  $result1 = mysqli_query($conn, $sql);

  $sql = "UPDATE `xiaoguandao_ais_tbl` SET shipname='$shipname', lon=$lon, lat=$lat, speed=$speed, course=$course, heading=$heading, 
  `status`='$status', callsign='$callsign', destination='$destination', shiptype='$shiptype', distance=$distance WHERE mmsi='$mmsi';";
  $result2 = mysqli_query($conn, $sql);
  // var_dump($sql, $result1, $result2, mysqli_error($conn));
  if($result1 and $result2){
    echo json_encode("{'msg':'success'}");
  }else{
    http_response_code(500);
    echo json_encode("{'error': '$error'}");
  }
?>