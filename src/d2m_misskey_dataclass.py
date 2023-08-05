import dataclasses
from enum import Enum
from typing import Any

class NoteVisibility(str, Enum):
    public = "public"
    home = "home"
    followers = "followers"
    specified = "specified"

class NoteReactionAcceptance(str, Enum):
    likeOnlyForRemote = "likeOnlyForRemote"
    nonSensitiveOnly = "nonSensitiveOnly"
    nonSensitiveOnlyForLocalLikeOnlyForRemote = "nonSensitiveOnlyForLocalLikeOnlyForRemote"
    likeOnly = "likeOnly"

@dataclasses.dataclass
class CreatableNote:
    i: str | None = None
    visibility: NoteVisibility | None = None
    visibleUserIds: list[str] | None = None
    cw: str | None = None
    localOnly: bool | None = None
    reactionAcceptance: NoteReactionAcceptance | None = None
    noExtractMentions: bool | None = None
    noExtractHashtags: bool | None = None
    noExtractEmojis: bool | None = None
    replyId: str | None = None
    renoteId: str | None = None
    channelId: str | None = None
    text: str | None = None
    fileIds: list[str] | None = None
    mediaIds: list[str] | None = None
    poll: dict[str, Any] | None = None
