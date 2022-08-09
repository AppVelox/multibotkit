from typing import Callable, Optional

from multibotkit.dispatchers.base_dispatcher import BaseDispatcher
from multibotkit.schemas.viber.incoming import Callback


class ViberDispatcher(BaseDispatcher):
    async def process_event(
        self, event: Callback
    ):
        state_id = f"viber_{event.user_id}"
        state_object = await self.state_manager.get_state(state_id)

        for (func, state_func, handler) in self._handlers:
            
            state_func_result = True
            if state_func is not None:
                try:
                    state_func_result = state_func(state_object)
                except Exception:
                    continue
            
            func_result = True
            if func is not None:
                try:
                    func_result = func(event)
                except Exception:
                    continue

            summary_result = state_func_result * func_result

            if summary_result:
                await handler(event, state_object)
                return
