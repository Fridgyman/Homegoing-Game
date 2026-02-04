import json

import pygame

from src.asset_manager import AssetManager
from src.camera import Camera
from src.dialogue import Monologue, Dialogue, MonologueOption, MonologueLine
from src.entity import Entity
from src.entity_route import EntityRoute, Waypoint
from src.event import DispatchEvent
from src.map_element import MapElement
from src.npc import NPC
from src.player import Player
from src.route_tracker import Conditions
from src.scene import Scene
from src.scene_in_out import SceneEntrance, SceneExit, str_to_scene_transition
from src.sprite import Sprite, copy_sprite
from src.ui_manager import UIManager


def parse_conditions(conditions_obj: dict) -> Conditions:
    all_flags: list[str] = [flag for flag in conditions_obj.get("all", [])]
    any_flags: list[str] = [flag for flag in conditions_obj.get("any", [])]
    not_flags: list[str] = [flag for flag in conditions_obj.get("not", [])]

    return Conditions(all_flags=all_flags, any_flags=any_flags, not_flags=not_flags)

def parse_entity_route(route_obj: dict) -> EntityRoute:
    waypoints_obj: list = route_obj.get("waypoints", [])
    waypoints: list[Waypoint] = []
    for waypoint_obj in waypoints_obj:
        face_dir: pygame.Vector2 = pygame.Vector2()
        match waypoint_obj.get("face_dir", ""):
            case "up":
                face_dir = pygame.Vector2(0, -1)
            case "down":
                face_dir = pygame.Vector2(0, 1)
            case "left":
                face_dir = pygame.Vector2(-1, 0)
            case "right":
                face_dir = pygame.Vector2(1, 0)
            case "":
                face_dir = pygame.Vector2(0, 1)

        waypoints.append(Waypoint(
            pos=pygame.Vector2(waypoint_obj.get("x", 0), waypoint_obj.get("y", 0)),
            speed=waypoint_obj.get("speed", 0),
            face_dir=face_dir,
            wait=waypoint_obj.get("wait", 0)
        ))

    conditions_obj: dict = route_obj.get("conditions", {})
    conditions: Conditions = parse_conditions(conditions_obj)

    return EntityRoute(waypoints=waypoints, conditions=conditions)

def parse_dispatch(dispatch_obj: dict) -> DispatchEvent:
    pass

def parse_monologue_option(option_obj: dict) -> MonologueOption:
    dispatch_events: list[DispatchEvent] = []
    dispatch_objs: list = option_obj.get("dispatch_on_select", [])
    for dispatch_obj in dispatch_objs:
        dispatch_events.append(parse_dispatch(dispatch_obj))

    modify_flags: list[tuple[str, str]] = []
    modify_flags_objs: list = option_obj.get("modify_flags_on_select", [])
    for modify_flags_obj in modify_flags_objs:
        modify_flags.append((modify_flags_obj.get("how", ""), modify_flags_obj.get("value", "")))

    set_route: list[tuple[str, Conditions]] = []
    set_routes_obj: list = option_obj.get("set_route_on_reach", [])
    for set_route_obj in set_routes_obj:
        set_route.append((
            set_route_obj.get("id", ""),
            parse_conditions(set_route_obj.get("conditions", {}))
        ))

    return MonologueOption(
        text=option_obj.get("text", ""),
        next_monologue=option_obj.get("next_monologue", ""),
        conditions=parse_conditions(option_obj.get("conditions", {})),
        dispatch=dispatch_events,
        modify_flags=modify_flags,
        set_route=set_route
    )

def parse_monologue(monologue_obj: dict) -> Monologue:
    conditions_obj: dict = monologue_obj.get("conditions", {})
    conditions: Conditions = parse_conditions(conditions_obj)

    lines: list[MonologueLine] = []
    lines_obj: list = monologue_obj.get("lines", [])
    for line_obj in lines_obj:
        lines.append(MonologueLine(
            text=line_obj.get("text", ""),
            speed=line_obj.get("char_time", 0)
        ))

    set_route: list[tuple[str, Conditions]] = []
    set_routes_obj: list = monologue_obj.get("set_route_on_reach", [])
    for set_route_obj in set_routes_obj:
        set_route.append((
            set_route_obj.get("id", ""),
            parse_conditions(set_route_obj.get("conditions", {}))
        ))

    dispatch_events: list[DispatchEvent] = []
    dispatch_objs: list = monologue_obj.get("dispatch_on_reach", [])
    for dispatch_obj in dispatch_objs:
        dispatch_events.append(parse_dispatch(dispatch_obj))

    options: list[MonologueOption] = []
    options_obj: dict = monologue_obj.get("options", {})
    for option_obj in options_obj:
        options.append(parse_monologue_option(option_obj))

    speaker_image: pygame.Surface | None = None
    if monologue_obj.get("speaker_image", "") != "":
        speaker_image = AssetManager.get_image(monologue_obj.get("speaker_image", ""))

    speaking_sfx: pygame.mixer.Sound | None = None
    if monologue_obj.get("speaking_sfx", "") != "":
        speaking_sfx = AssetManager.get_audio(monologue_obj.get("speaking_sfx", ""))

    return Monologue(
        conditions=conditions,
        alt_monologue=monologue_obj.get("alt_monologue", ""),
        speaker=monologue_obj.get("speaker", ""),
        lines=lines,
        font=AssetManager.get_font(monologue_obj.get("font", "")),
        next_monologue=monologue_obj.get("next_monologue", None),
        set_route=set_route,
        dispatch=dispatch_events,
        options=options,
        speaker_image=speaker_image,
        speaking_sfx=speaking_sfx
    )


def parse_dialogue(dialogue_obj: dict, entity_id: str) -> Dialogue:
    modify_flags: list[tuple[str, str]] = []
    modify_flags_objs: list = dialogue_obj.get("modify_flags_on_start", [])
    for modify_flags_obj in modify_flags_objs:
        modify_flags.append((modify_flags_obj.get("how", ""), modify_flags_obj.get("value", "")))

    dispatch_events: list[DispatchEvent] = []
    dispatch_objs: list = dialogue_obj.get("dispatch_on_start", [])
    for dispatch_obj in dispatch_objs:
        dispatch_events.append(parse_dispatch(dispatch_obj))

    start_monologues: list[tuple[str, Conditions]] = []
    start_monologues_obj: list = dialogue_obj.get("start_monologue", [])
    for start_monologue_obj in start_monologues_obj:
        start_monologues.append((
            start_monologue_obj.get("id", ""),
            parse_conditions(start_monologue_obj.get("conditions", {}))
        ))

    monologues: dict[str, Monologue] = {}
    monologues_obj: list = dialogue_obj.get("monologues", [])
    for monologue_obj in monologues_obj:
        monologues[monologue_obj.get("id", "")] = parse_monologue(monologue_obj)

    return Dialogue(
        conditions=parse_conditions(dialogue_obj.get("conditions", {})),
        modify_flags=modify_flags,
        dispatch=dispatch_events,
        start_monologues=start_monologues,
        monologues=monologues,
        entity_id=entity_id
    )


def parse_scene(scene_obj: dict) -> Scene:
    void_color_obj: dict = scene_obj.get("void_color", {})
    void_color: tuple[int, int, int, int] = (
        void_color_obj.get("r", 0), void_color_obj.get("g", 0), void_color_obj.get("b", 0),
        void_color_obj.get("a", 0)
    )

    bounds_obj: dict = scene_obj.get("bounds")
    bounds = pygame.Vector2(bounds_obj.get("x", 0), bounds_obj.get("y", 0))

    background_music_obj: dict = scene_obj.get("background_music", {})
    background_music: pygame.mixer.Sound = AssetManager.get_audio(background_music_obj.get("identifier", ""))
    background_music.set_volume(background_music_obj.get("volume", 1))

    map_elements_obj: list = scene_obj.get("map_elements", [])
    map_elements: list[MapElement] = []
    for map_element_obj in map_elements_obj:
        rect_obj: dict = map_element_obj.get("rect", {})
        rect: pygame.Rect = pygame.Rect(rect_obj.get("x", 0), rect_obj.get("y", 0),
                                        rect_obj.get("w", 0), rect_obj.get("h", 0))
        map_elements.append(MapElement(
            rect=rect,
            image=AssetManager.get_image(map_element_obj.get("image", "")),
            collision=map_element_obj.get("collision", False)
        ))

    entity_lookup: dict = {}
    entity_lookup_obj: list = scene_obj.get("entity_lookup", [])
    for lookup_entry_obj in entity_lookup_obj:
        sprite: Sprite = copy_sprite(AssetManager.get_sprite(lookup_entry_obj.get("sprite", "")))
        sprite.set_default_anim(lookup_entry_obj.get("default_animation", ""))
        sprite.set_frame_time(lookup_entry_obj.get("animation_frame_time", 0))

        entity_lookup[lookup_entry_obj.get("id")] = (
            sprite,
            lookup_entry_obj.get("collision", False)
        )

    player_obj: dict = scene_obj.get("player", {})
    player_fallback_spawn: dict = player_obj.get("fallback_spawn", {})
    player = Player(
        spawn=pygame.Vector2(player_fallback_spawn.get("x", 0), player_fallback_spawn.get("y", 0)),
        sprite=copy_sprite(entity_lookup.get(player_obj.get("lookup", ""))[0]),
        move_duration=player_obj.get("move_duration", 0)
    )

    entrances: dict[str, SceneEntrance] = {}
    entrances_obj: list = scene_obj.get("entrances", [])
    for entrance_obj in entrances_obj:
        spawn_obj: dict = entrance_obj.get("spawn", {})
        entrances[entrance_obj.get("identifier", "")] = SceneEntrance(
            spawn=pygame.Vector2(spawn_obj.get("x", 0), spawn_obj.get("y", 0)),
            transition=str_to_scene_transition(entrance_obj.get("transition", "")),
            transition_time=entrance_obj.get("transition_time", 0)
        )

    exits: list[SceneExit] = []
    exits_obj: list = scene_obj.get("exits", [])
    for exit_obj in exits_obj:
        rect_obj: dict = exit_obj.get("rect", {})
        rect: pygame.Rect = pygame.Rect(
            rect_obj.get("x", 0), rect_obj.get("y", 0), rect_obj.get("w", 0), rect_obj.get("h", 0)
        )

        exits.append(SceneExit(
            rect=rect,
            require_interact=exit_obj.get("require_interact", False),
            transition=str_to_scene_transition(exit_obj.get("transition", "")),
            transition_time=exit_obj.get("transition_time", 0),
            next_scene=exit_obj.get("next_scene", ""),
            next_entrance=exit_obj.get("entrance", ""),
            conditions=parse_conditions(exit_obj.get("conditions", {}))
        ))

    entities: dict[str, Entity] = {}

    entities_obj: list = scene_obj.get("entities", [])
    for entity_obj in entities_obj:
        conditions_obj: dict = entity_obj.get("conditions", {})
        conditions: Conditions = parse_conditions(conditions_obj)

        dialogues: dict[str, Dialogue] = {}
        dialogues_obj: list = entity_obj.get("dialogues", [])
        for dialogue_obj in dialogues_obj:
            dialogues[dialogue_obj.get("id", "")] = parse_dialogue(dialogue_obj, entity_obj.get("id", ""))

        routes: dict[str, EntityRoute] = {}
        routes_obj: list = entity_obj.get("routes", [])
        for route_obj in routes_obj:
            routes[route_obj.get("id", "")] = parse_entity_route(route_obj)

        if len(dialogues) > 0:
            spawn_obj: dict = entity_obj.get("spawn", {})
            new_npc: NPC = NPC(
                sprite=copy_sprite(entity_lookup.get(entity_obj.get("lookup", ""))[0]),
                collision=entity_lookup.get(entity_obj.get("lookup", ""))[1],
                spawn=pygame.Vector2(spawn_obj.get("x", 0), spawn_obj.get("y", 0)),
                conditions=conditions,
                routes=routes,
                dialogues=dialogues
            )
            entities[entity_obj.get("id", "")] = new_npc
        else:
            spawn_obj: dict = entity_obj.get("spawn", {})
            new_entity: Entity = Entity(
                sprite=copy_sprite(entity_lookup.get(entity_obj.get("lookup", ""))[0]),
                collision=entity_lookup.get(entity_obj.get("lookup", ""))[1],
                spawn=pygame.Vector2(spawn_obj.get("x", 0), spawn_obj.get("y", 0)),
                conditions=conditions,
                routes=routes
            )
            entities[entity_obj.get("id", "")] = new_entity

    scene: Scene = Scene(
        void_color=void_color,
        bounds=bounds,
        background_music=background_music,
        map_elements=map_elements,
        player=player,
        entities=entities,
        entrances=entrances,
        exits=exits
    )

    return scene


class SceneManager:
    def __init__(self, scene_guide: str):
        self.scenes: dict[str, Scene] = {}
        self.current_scene: str = ""

        self.fade = 0
        self.fading = 0

        self.overlay: pygame.Surface = pygame.Surface(pygame.display.get_window_size()).convert()
        self.overlay.fill((0, 0, 0))

        with open(scene_guide, "r") as file:
            obj = json.load(file)

        for scene_obj in obj.get("effia", {}).get("scenes", []):
            with open(scene_obj.get("path"), "r") as file:
                scene_json = json.load(file)
            self.add_scene(scene_obj.get("name"), parse_scene(scene_json))

    def add_scene(self, name: str, scene: Scene) -> None:
        self.scenes[name] = scene

    def load_scene(self, scene_name: str, entrance_id: str, player_face_dir: pygame.Vector2) -> None:
        if self.current_scene != "":
            self.scenes[self.current_scene].unload()
        self.scenes[scene_name].load(entrance_id, player_face_dir)
        self.current_scene = scene_name

    def input(self, ui_manager: UIManager, keys: pygame.key.ScancodeWrapper) -> None:
        self.scenes[self.current_scene].input(ui_manager, keys)

    def update(self, camera: Camera, ui_manager: UIManager, dt: float) -> None:
        self.fade = pygame.math.clamp(self.fade + self.fading * dt, 0, 255)
        self.scenes[self.current_scene].update(camera, ui_manager, dt, self)

    def render(self, window_surface: pygame.Surface, camera: Camera, ui_manager: UIManager) -> None:
        self.scenes[self.current_scene].render(window_surface, camera, ui_manager)

        if self.fade > 0:
            self.overlay.set_alpha(self.fade)
            window_surface.blit(self.overlay, (0, 0))
