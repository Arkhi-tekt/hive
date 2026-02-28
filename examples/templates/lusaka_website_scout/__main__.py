import asyncio
import argparse
import json
from .agent import default_agent

async def main():
    parser = argparse.ArgumentParser(description="Run the Lusaka Website Scout Agent")
    parser.add_argument("--category", type=str, default="Law firms in Lusaka", help="Category of businesses to search for")
    args = parser.parse_args()

    print(f"🚀 Starting Lusaka Website Scout for category: {args.category}...")

    context = {"business_category": args.category}
    result = await default_agent.run(context)

    if result.success:
        print("\n✅ Scout Finished Successfully!")
    else:
        print(f"\n❌ Scout Failed: {result.error}")

if __name__ == "__main__":
    asyncio.run(main())
