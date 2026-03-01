import asyncio, sys 
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.services.scenario_factory import create_scenario

async def main():
    scenario = await create_scenario(level=1)
    print(scenario.statement)

asyncio.run(main())