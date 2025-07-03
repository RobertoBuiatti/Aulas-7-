extends Node2D

@onready var gorwth_timer: Timer = $pickable_area/gorwth_timer
@onready var animated_sprite_2d: AnimatedSprite2D = $AnimatedSprite2D
@onready var marker_2d: Marker2D = $Marker2D

var state = "no apples"
var player_in_area = false

var apple = preload("res://scene/apple_collectable.tscn")

@export var item: InvItem
var player = null


func _ready() -> void:
	if state == "no apples":
		gorwth_timer.start()



func _process(delta: float) -> void:
	if state == "no apples":
		animated_sprite_2d.play("no apples")
	if state == "apples":
		if player_in_area:
			if Input.is_action_just_pressed("e"):
				state = "no apples"
				drop_apple()
		animated_sprite_2d.play("apples")



func _on_pickable_area_body_entered(body: Node2D) -> void:
	if body.has_method("player"):
		player_in_area = true
		player = body


func _on_pickable_area_body_exited(body: Node2D) -> void:
	if body.has_method("player"):
		player_in_area = false


func _on_gorwth_timer_timeout() -> void:
	if state == "no apples":
		state = "apples"

func drop_apple():
	var apple_instance = apple.instantiate()
	apple_instance.global_position = marker_2d.global_position
	get_parent().add_child(apple_instance)
	player.collect(item)
	await get_tree().create_timer(3).timeout
	gorwth_timer.start()
