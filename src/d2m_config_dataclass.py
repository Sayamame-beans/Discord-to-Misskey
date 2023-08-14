from __future__ import annotations

import dataclasses
import types
import typing
from typing import Any

@dataclasses.dataclass
class d2mConfigImpl:
    pass

    # Based on https://zenn.dev/yosemat/articles/2fce02d2ad0794
    # To be strict, field_type can be type, types.GenericAlias, types.UnionType, typing.Any, or any other.
    # Here, minimum runtime type checks are performed.
    @classmethod
    def from_dict(cls, src: dict[str, int | str | list[Any] | dict[str, Any]]) -> d2mConfig | d2mConfigDiscord | d2mConfigDiscordChannel | d2mConfigMisskey | d2mConfigImpl:
        kwargs: dict[str, Any] = dict()
        field_dict: dict[str, dataclasses.Field[Any]] = {field.name: field for field in dataclasses.fields(cls)}
        field_type_dict: dict[str, type | types.GenericAlias] = typing.get_type_hints(cls)

        for src_key, src_value in src.items():
            if src_key not in field_dict:
                raise KeyError(src_key)

            field_type = field_type_dict[field_dict[src_key].name]

            if issubclass(field_type, d2mConfigImpl):
                if isinstance(src_value, dict):
                    kwargs[src_key] = field_type.from_dict(src_value)
                else:
                    raise TypeError(f"\"{src_key}\" value must be dict, not {type(src_value).__name__}")
            elif isinstance(field_type, types.GenericAlias): #whether list[] or not
                if isinstance(src_value, field_type.__origin__):
                    for element in src_value:
                        if not isinstance(element, dict):
                            raise TypeError(f"\"{src_key}\" value must be list of dict, not list of {type(element).__name__}")
                    kwargs[src_key] = [field_type.__args__[0].from_dict(element) for element in src_value]
                else:
                    raise TypeError(f"\"{src_key}\" value must be {field_type.__name__}, not {type(src_value).__name__}")
            elif isinstance(src_value, field_type) and not issubclass(type(src_value), bool):
                kwargs[src_key] = src_value
            else:
                raise TypeError(f"\"{src_key}\" value must be {field_type.__name__}, not {type(src_value).__name__}")

        return cls(**kwargs)

@dataclasses.dataclass
class d2mConfigDiscordChannel(d2mConfigImpl):
    guild_id: int = 0
    channel_id: int = 0

@dataclasses.dataclass
class d2mConfigDiscord(d2mConfigImpl):
    token: str = ""
    forward_targets: list[d2mConfigDiscordChannel] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class d2mConfigMisskey(d2mConfigImpl):
    host_url: str = ""
    token: str = ""

@dataclasses.dataclass
class d2mConfig(d2mConfigImpl):
    discord: d2mConfigDiscord = dataclasses.field(default_factory=d2mConfigDiscord)
    misskey: list[d2mConfigMisskey] = dataclasses.field(default_factory=list)
