"""Debug the SOGo 6 login flow to identify what's failing."""
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})

        messages = []
        page.on("console", lambda msg: messages.append(f"[CONSOLE] {msg.type}: {msg.text[:200]}"))
        page.on("pageerror", lambda err: messages.append(f"[PAGE_ERR] {err}"))
        page.on("requestfailed", lambda req: messages.append(f"[REQ_FAIL] {req.url[:100]} {req.failure}"))
        page.on("response", lambda resp: messages.append(f"[RESP] {resp.status} {resp.url[:80]}") if resp.status >= 400 else None)

        await page.goto("http://localhost:3000/en/auth/login", wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)
        print(f"Login page: {page.url}")

        # Check form structure
        info = await page.evaluate("""() => {
            const form = document.querySelector('form');
            if (!form) return JSON.stringify({error: 'no form'});
            const inputs = Array.from(form.querySelectorAll('input, button'));
            return JSON.stringify({
                action: form.action,
                method: form.method,
                inputs: inputs.map(el => ({
                    tag: el.tagName,
                    id: el.id,
                    name: el.name,
                    type: el.type,
                    placeholder: el.placeholder,
                }))
            });
        }""")
        print(f"Form: {info}")

        # Fill email and submit
        email_input = page.locator("input[type='email'], input#email, input[name='email']").first
        print(f"Email input visible: {await email_input.is_visible()}")
        await email_input.fill("testuser@example.org")
        await page.wait_for_timeout(500)

        # Try clicking the submit button
        submit_btn = page.locator("button[type='submit']")
        print(f"Submit btn visible: {await submit_btn.is_visible()}")
        await submit_btn.click()
        await page.wait_for_timeout(3000)
        print(f"After email submit: {page.url}")

        # Password step
        pwd = page.locator("input[type='password']")
        if await pwd.is_visible(timeout=5000):
            print("Password field found, filling...")
            await pwd.fill("password123")
            await page.wait_for_timeout(500)
            await submit_btn.click()
            await page.wait_for_timeout(5000)
            print(f"After password: {page.url}")

            # Wait longer for redirect
            for i in range(20):
                await page.wait_for_timeout(1000)
                url = page.url
                if "/u/" in url:
                    print(f"Redirected to: {url}")
                    break
            else:
                print(f"No redirect. Final URL: {page.url}")
                body_text = await page.evaluate("() => document.body.innerText.substring(0, 1000)")
                print(f"Body: {body_text}")
        else:
            print("Password field NOT found!")
            body_text = await page.evaluate("() => document.body.innerText.substring(0, 500)")
            print(f"Body: {body_text}")

        print("\n=== Browser messages (last 15) ===")
        for msg in messages[-15:]:
            print(msg)

        await browser.close()

asyncio.run(main())
