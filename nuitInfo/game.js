function Point(x, y) {
    this.x = x;
    this.y = y;
}
Point.prototype.x = null;
Point.prototype.y = null;

function produit_vectoriel(point1, point2, point3) {
    return Math.sqrt(point1*point1 + point2*point2) * Math.sqrt(point1*point1 + point3*point3) * Math.sqrt(point2*point2 + point3*point3) / Math.sqrt(point1*point1 + point3*point3)
}

function intersection(p0_x, p0_y, p1_x, p1_y,
    p2_x, p2_y, p3_x, p3_y)
{
    var s1_x, s1_y, s2_x, s2_y;
    s1_x = p1_x - p0_x;     s1_y = p1_y - p0_y;
    s2_x = p3_x - p2_x;     s2_y = p3_y - p2_y;

    var s, t;
    s = (-s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) / (-s2_x * s1_y + s1_x * s2_y);
    t = ( s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) / (-s2_x * s1_y + s1_x * s2_y);

    return s >= 0 && s <= 1 && t >= 0 && t <= 1
}

var Directions = {
    left: 0,
    right: 1,
    up: 2,
    down: 3
};

(function(){
    var gameZone = document.getElementById("gameZone");
    gameZone.width = document.body.clientWidth;
    gameZone.height = document.body.clientHeight;

    var context = gameZone.getContext("2d");

    var default_size = 100;
    var player = {
        width: 10,
        speed: 2,
        direction: Directions.up,
        points: [new Point(document.body.clientWidth / 2, document.body.clientHeight / 2 - default_size),
            new Point(document.body.clientWidth / 2, document.body.clientHeight / 2)]
    };

    document.onkeydown = function(event) {
        switch(event.key) {
            case "ArrowLeft":
                if(player.direction === Directions.left || player.direction === Directions.right) {return}
                player.direction = Directions.left;
                break;
            case "ArrowRight":
                if(player.direction === Directions.left || player.direction === Directions.right) {return}
                player.direction = Directions.right;
                break;
            case "ArrowUp":
                if(player.direction === Directions.up || player.direction === Directions.down) {return}
                player.direction = Directions.up;
                break;
            case "ArrowDown":
                if(player.direction === Directions.up || player.direction === Directions.down) {return}
                player.direction = Directions.down;
                break;
            default:
                return;
        }
        var tmp = [new Point(player.points[0].x, player.points[0].y)];
        Array.prototype.push.apply(tmp, player.points);
        player.points = tmp;
    };

    function on_enter_frame(){
    	context.clearRect(0, 0, gameZone.clientWidth, gameZone.clientHeight);
        context.lineWidth = 20;
        context.lineJoin = "round";
        context.setLineDash([20, 2]);
        context.beginPath();
        context.moveTo(player.points[0].x, player.points[0].y);
        player.points.forEach(function(l) {
            context.lineTo(l.x, l.y);
        });
        context.stroke();
    	context.closePath();
        switch (player.direction) {
            case Directions.left:
                player.points[0].x -= player.speed;
                break;
            case Directions.right:
                player.points[0].x += player.speed;
                break;
            case Directions.up:
                player.points[0].y -= player.speed;
                break;
            case Directions.down:
                player.points[0].y += player.speed;
                break;
        }
        if(player.points[player.points.length - 1].y === player.points[player.points.length - 2].y) {
            // left
            if(player.points[player.points.length - 1].x >= player.points[player.points.length - 2].x) {
                player.points[player.points.length - 1].x -= player.speed;
                if(player.points[player.points.length - 1].x < player.points[player.points.length - 2].x) {
                 player.points.pop();
                 }
            }
            // right
            else if(player.points[player.points.length - 1].x <= player.points[player.points.length - 2].x) {
                player.points[player.points.length - 1].x += player.speed;
                if(player.points[player.points.length - 1].x > player.points[player.points.length - 2].x) {
                 player.points.pop();
                 }
            }
        } else {
            // up
            if (player.points[player.points.length - 1].y >= player.points[player.points.length - 2].y) {
                player.points[player.points.length - 1].y -= player.speed;
                if(player.points[player.points.length - 1].y < player.points[player.points.length - 2].y) {
                 player.points.pop();
                 }
            }
            // down
            else if (player.points[player.points.length - 1].y <= player.points[player.points.length - 2].y) {
                player.points[player.points.length - 1].y += player.speed;
                if(player.points[player.points.length - 1].y > player.points[player.points.length - 2].y) {
                 player.points.pop();
                 }
            }
        }

        if(player.points.length >= 5) {
            for (var i = 0; i < player.points.length - 4; i++) {
                for (var j = i + 1; j < player.points.length - 1; j++) {
                    //vertical
                    if(player.points[i].x === player.points[i + 1].x && player.points[j].x === player.points[j + 1].x) {
                        continue
                    }
                    if(player.points[i].y === player.points[i + 1].y && player.points[j].y === player.points[j + 1].y) {
                        continue
                    }
                    if (intersection(player.points[i].x, player.points[i].y, player.points[i + 1].x, player.points[i + 1].y, player.points[j].x, player.points[j].y, player.points[j + 1].x, player.points[j + 1].y)) {
                        player = {
                            width: 10,
                            speed: 2,
                            direction: Directions.up,
                            points: [new Point(document.body.clientWidth / 2, document.body.clientHeight / 2 - default_size),
                                new Point(document.body.clientWidth / 2, document.body.clientHeight / 2)]
                        };
                    }
                }
            }
        }

        if(player.points[0].x <= 0 || player.points[0].x >= document.body.clientWidth ||
            player.points[0].y <= 0 || player.points[0].y >= document.body.clientHeight) {
            player = {
                width: 10,
                speed: 2,
                direction: Directions.up,
                points: [new Point(document.body.clientWidth / 2, document.body.clientHeight / 2 - default_size),
                    new Point(document.body.clientWidth / 2, document.body.clientHeight / 2)]
            };
        }
    }

    setInterval(on_enter_frame, 1000/60);
})();
