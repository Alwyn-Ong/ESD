
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Demo Site</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <link rel="stylesheet" href="css/bootstrap.css" type='text/css'>
</head>
<body>
<header>
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
        <a class="navbar-brand" href="#">SGLoveLah</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse justify-content-end" id="navbarSupportedContent">
            <ul class="navbar-nav">
            <li class="nav-item active">
                    <a class="nav-link" href="Discover.php">Discover</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="Matches.php">Matches</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="../chat.html">Chat</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="../account.html">Account</a>
                </li>
            </ul>
        </div>
    </nav>
    <br>
    <!-- <section class="py-2">
        <div class="container">
            <h3 class="text-uppercase font-weight-light text-center m-5">Discover</h3>
        </div>
        
        Filter By: <input type="text" id="myText" placeholder="Enter Age" class="filter">
    </section>
    <div id="carouselExampleIndicators" class="carousel slide" data-ride="carousel">
        <ol class="carousel-indicators">
            <li data-target="#carouselExampleIndicators" data-slide-to="0" class="active"></li>
            <li data-target="#carouselExampleIndicators" data-slide-to="1"></li>
            <li data-target="#carouselExampleIndicators" data-slide-to="2"></li>
        </ol>
        <div class="carousel-inner">
            <div class = "row">
                <div class="carousel-item active">
                    <div class="hi">
                        <img class="img" src="img/dating_3.jpg" alt="First slide">
                        <div class="container-fluid">
                            <div class="carousel-caption">
                            <h1>Meaningful Relationship</h1>
                            <p class="lead">Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.</p>
                            <a class="btn btn-large btn-primary" href="#">Sign up today</a>
                            </div>
                        </div>
                    </div>
                </div>  
            
                <div class="carousel-item">
                        <div class="mbr-overlay">
                            <img class="d-block w-100" src="img/dating_2.jpg" alt="Second slide">
                            <div class="container-fluid">
                                <div class="carousel-caption">
                                <h1>Create Connections</h1>
                                <p class="lead">Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.</p>
                                <a class="btn btn-large btn-primary" href="#">Sign up today</a>
                                </div>
                            </div>
                        </div>
                </div>

                <div class="carousel-item">
                    <div class="mbr-overlay">
                        <img class="d-block w-100" src="img/dating_1.jpg" alt="Third slide">
                        <div class="container-fluid">
                            <div class="carousel-caption">
                            <h1 style="black">Lasting Friendships</h1>
                            <p class="lead">Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.</p>
                            <a class="btn btn-large btn-primary" href="#">Sign up today</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <a class="carousel-control-prev" href="#carouselExampleIndicators" role="button" data-slide="prev">
            <span class="carousel-control-prev-icon"></span>
        </a>
        <a class="carousel-control-next" href="#carouselExampleIndicators" role="button" data-slide="next">
            <span class="carousel-control-next-icon"></span>
        </a>
    </div> -->


<section class="py-2">
    <div class="container">
        <h3 class="text-uppercase font-weight-light text-center m-5">Discover</h3>

        <div class="row justify-content-center">
            <div class="col-8">
                <div class="card ">
                    <?php
                        $image_new = "img\dating_3";
                        if(!isset($_GET["Like"])){
                            echo "<img class=\"card-img-top\" src=\"https://source.unsplash.com/collection/190727/1400x700\" alt=\"Card image cap\">";
                        } else {
                            echo "<img class=\"card-img-top\" src=\"$image_new\" alt=\"Card image cap\">";
                        }
                         
                    ?>
                    <!-- <img class="card-img-top" src="https://source.unsplash.com/collection/190727/1400x700" alt="Card image cap"> -->
                    <div class="card-body">
                        <h5 class="card-title">Card title</h5>
                        <p class="card-text">This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>
                    </div>
                    <div class="card-footer">
                        <small class="text-muted">Posted on 07/03/2020</small>
                    </div>
                </div>
            </div>

            <!-- <div class="col-12 col-md-4 mb-4 mb-md-0">
                <div class="card">
                    <img class="card-img-top" src="https://source.unsplash.com/collection/190727/1400x700" alt="Card image cap">
                    <div class="card-body">
                        <h5 class="card-title">Card title</h5>
                        <p class="card-text">This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>
                    </div>
                    <div class="card-footer">
                        <small class="text-muted">Posted on 21/02/2020</small>
                    </div>
                </div>
            </div>

            <div class="col-12 col-md-4">
                <div class="card">
                    <img class="card-img-top" src="https://source.unsplash.com/collection/190727/1400x700" alt="Card image cap">
                    <div class="card-body">
                        <h5 class="card-title">Card title</h5>
                        <p class="card-text">This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>
                    </div>
                    <div class="card-footer">
                        <small class="text-muted">Posted on 12/01/2020</small>
                    </div>
                </div>
            </div> -->
        </div>
    </div>
    <br>
    <form action="Discover.php">
    <div class="text-center" >
        <button style="width:100px;" type="submit" onclick="likeSelected()" value = "Like" class="btn btn-status" name="Like">Like</button>
        <button style="width:100px; background-color:#800000;" type="button" value = "notLike" class="btn btn-status" name="notLike">Dislike</button>
    </div>
    </form>
</section>
</header>


<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</body>


</html>



