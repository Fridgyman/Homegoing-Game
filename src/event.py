import enum

import pygame


class SceneState(enum.Enum):
    ENTERING = 0,
    ENTERED = 1,
    EXITING = 2,
    EXITED = 3

class CatchEvent:
    def __init__(self):
        pass

    def catch(self, scene) -> bool:
        pass

class DispatchEvent:
    def __init__(self):
        self.dispatched: bool = False

    def dispatch(self, scene) -> None:
        self.dispatched = True

    def update(self, scene, dt: float) -> None:
        pass


class OnPlayerEnter(CatchEvent):
    def __init__(self, rect: pygame.Rect):
        super().__init__()
        self.rect: pygame.Rect = rect

    def catch(self, scene) -> bool:
        return self.rect.collidepoint(scene.player.grid_pos)

class OnEntityEnter(CatchEvent):
    def __init__(self, ids: list[str], rect: pygame.Rect):
        super().__init__()
        self.ids: list[str] = ids
        self.rect: pygame.Rect = rect

    def catch(self, scene) -> bool:
        for identifier in self.ids:
            if (entity := scene.entities.get(identifier, None)) is not None and \
                    self.rect.colliderect(entity.grid_pos, entity.hit_box):
                return True
        return False

class OnSceneStart(CatchEvent):
    def __init__(self):
        super().__init__()

    def catch(self, scene) -> bool:
        return scene.state == SceneState.ENTERED

class OnSceneExit(CatchEvent):
    def __init__(self):
        super().__init__()

    def catch(self, scene) -> bool:
        return scene.state == SceneState.EXITED


class AddEntity(DispatchEvent):
    def __init__(self, ids: list[str]):
        super().__init__()
        self.ids: list[str] = ids

    def dispatch(self, scene) -> None:
        pass

class RemoveEntity(DispatchEvent):
    def __init__(self, ids: list[str]):
        super().__init__()
        self.ids: list[str] = ids

    def dispatch(self, scene) -> None:
        pass

class SetEntityRoute(DispatchEvent):
    def __init__(self, entity_id: str, route_id: str):
        super().__init__()
        self.entity_id: str = entity_id
        self.route_id: str = route_id

    def dispatch(self, scene) -> None:
        pass

class StartEntityAnimation(DispatchEvent):
    def __init__(self, entity_id: str, animation_name: str):
        super().__init__()
        self.entity_id: str = entity_id
        self.animation_name: str = animation_name

    def dispatch(self, scene) -> None:
        pass

class StopEntityAnimation(DispatchEvent):
    def __init__(self, entity_id: str):
        super().__init__()
        self.entity_id: str = entity_id

    def dispatch(self, scene) -> None:
        pass

class BeginEntityDialogue(DispatchEvent):
    def __init__(self, entity_id: str, dialogue_id: str):
        super().__init__()
        self.entity_id: str = entity_id
        self.dialogue_id: str = dialogue_id

    def dispatch(self, scene) -> None:
        pass

class BeginIndependentDialogue(DispatchEvent):
    def __init__(self, dialogue):
        super().__init__()
        self.dialogue = dialogue

    def dispatch(self, scene) -> None:
        pass

class EndDialogueAbruptly(DispatchEvent):
    def __init__(self):
        super().__init__()

    def dispatch(self, scene) -> None:
        pass

class MoveCameraPosition(DispatchEvent):
    def __init__(self, pos: pygame.Vector2):
        super().__init__()
        self.pos: pygame.Vector2 = pos

    def dispatch(self, scene) -> None:
        pass

class MoveCameraEntity(DispatchEvent):
    def __init__(self, entity_id: str):
        super().__init__()
        self.entity_id: str = entity_id

    def dispatch(self, scene) -> None:
        pass

class MoveCameraFollowEntity(DispatchEvent):
    def __init__(self, entity_id: str):
        super().__init__()
        self.entity_id: str = entity_id

    def dispatch(self, scene) -> None:
        pass

class MovePlayer(DispatchEvent):
    def __init__(self, waypoints: list[pygame.Vector2]):
        super().__init__()
        self.waypoints: list[pygame.Vector2] = waypoints

    def dispatch(self, scene) -> None:
        pass

class EntityFollowPlayer(DispatchEvent):
    def __init__(self, entity_id: str):
        super().__init__()
        self.entity_id: str = entity_id

    def dispatch(self, scene) -> None:
        pass

class EntityFollowEntity(DispatchEvent):
    def __init__(self, lead_entity_id: str, follow_entity_id: str):
        super().__init__()
        self.lead_entity_id: str = lead_entity_id
        self.follow_entity_id: str = follow_entity_id

    def dispatch(self, scene) -> None:
        pass

class ResetCamera(DispatchEvent):
    def __init__(self):
        super().__init__()

    def dispatch(self, scene) -> None:
        pass

class ShakeCamera(DispatchEvent):
    def __init__(self, time: float):
        super().__init__()
        self.time: float = time

    def dispatch(self, scene) -> None:
        pass

class EndCameraShake(DispatchEvent):
    def __init__(self):
        super().__init__()

    def dispatch(self, scene) -> None:
        pass

class BlinkCamera(DispatchEvent):
    def __init__(self):
        super().__init__()

    def dispatch(self, scene) -> None:
        pass

class PlayAudio(DispatchEvent):
    def __init__(self, audio_id: str, volume: float):
        super().__init__()
        self.audio_id: str = audio_id
        self.volume: float = volume

    def dispatch(self, scene) -> None:
        pass

class FadeAudioVolume(DispatchEvent):
    def __init__(self, fraction: float):
        super().__init__()
        self.fraction: float = fraction

    def dispatch(self, scene) -> None:
        pass

class EnableTrigger(DispatchEvent):
    def __init__(self, trigger_id: str):
        super().__init__()
        self.trigger_id: str = trigger_id

    def dispatch(self, scene) -> None:
        pass

class DisableTrigger(DispatchEvent):
    def __init__(self, trigger_id: str):
        super().__init__()
        self.trigger_id: str = trigger_id

    def dispatch(self, scene) -> None:
        pass