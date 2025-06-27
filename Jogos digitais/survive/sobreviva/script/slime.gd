extends CharacterBody2D

@onready var detection_area: CollisionShape2D = $detection_area/CollisionShape2D
@onready var animated_sprite_2d: AnimatedSprite2D = $AnimatedSprite2D
@onready var hitbox: CollisionShape2D = $hitbox/CollisionShape2D
@onready var slime_collect_area: CollisionShape2D = $slime_collect_area/CollisionShape2D

var speed = 50.0
var health = 100

var dead = false
var player_in_area = false
var player

@onready var slime: StaticBody2D = $slime_collectable
@export var itemRes: InvItem

func _ready():
	dead = false

func _physics_process(delta):
	if !dead:
		detection_area.disabled = false
		if player_in_area:
			var direction = (player.position - position).normalized()
			velocity = direction * speed
			move_and_slide()
			animated_sprite_2d.play("move")
		else:
			velocity = Vector2.ZERO
			move_and_slide()
			animated_sprite_2d.play("idle")
	else:
		detection_area.disabled = true
		velocity = Vector2.ZERO
		move_and_slide()

func _on_detection_area_body_entered(body: Node2D) -> void:
	if body.has_method("player"):
		player_in_area = true
		player = body


func _on_detection_area_body_exited(body: Node2D) -> void:
	if body.has_method("player"):
		player_in_area = false
		player = body


func _on_hitbox_area_entered(area: Area2D) -> void:
	var damage
	if area.has_method("arrow_deal_damage"):
		damage = 50
		take_damage(damage)

func take_damage(damage):
	health = health - damage
	if health <=0 and !dead:
		death()

func death():
	dead = true
	animated_sprite_2d.play("death")
	await get_tree().create_timer(1).timeout
	drop_slime()
	
	animated_sprite_2d.visible = false
	hitbox.disabled = true
	detection_area.disabled = true

func drop_slime():
	slime.visible = true
	slime_collect_area.disabled = false
	slime_collect()
	
func slime_collect():
	await get_tree().create_timer(1.5).timeout
	slime.visible = false
	player.collect(itemRes)
	queue_free()


func _on_slime_collect_area_body_entered(body: Node2D) -> void:
	if body.has_method("player"):
		player = body
