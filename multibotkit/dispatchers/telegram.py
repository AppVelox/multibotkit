from multibotkit.dispatchers.base_dispatcher import BaseDispatcher
from multibotkit.schemas.telegram.incoming import Update


class TelegramDispatcher(BaseDispatcher):

    async def process_event(
        self, event: Update
    ):    
        if event.message is not None:
            sender_id = event.message.from_.id
        if event.callback_query is not None:
            sender_id = event.callback_query.from_.id
        
        state_id = f"telegram_{sender_id}"
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
