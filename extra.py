from bs4 import BeautifulSoup

html = """
<div class="accordion__content prose">
    <p><meta charset="utf-8"/><span>The Onyx Ring...</span></p>
    <p><em><strong>DETAILS</strong></em></p>
    <ul><li>Natural Onyx Gemstone</li></ul>
    <p><em><b>SIZE DETAILS</b></em></p>
    <p><em><strong>QUALITY ASSURANCE</strong></em></p>
    <p>This ring is made from Recycled Stainless Steel.</p>
    <p><em><strong>QUESTIONS?</strong></em></p>
    <p>If you have a questions or want to know more about this piece, email us at help@twistedpendant.co.uk</p>
</div>
"""

soup = BeautifulSoup(html, "html.parser")

# Find the <p> that contains "QUESTIONS"
target_p = soup.find("p", string=lambda t: t and "QUESTIONS" in t)

if target_p:
    # Remove the target <p>
    target_p.decompose()

    # Find the next <p> sibling (the one just under it)
    contactInfo = soup.find("p", string=lambda t: t and "@" in t)
    if contactInfo:
        contactInfo.decompose()

# Print the updated HTML
print(soup.prettify())
