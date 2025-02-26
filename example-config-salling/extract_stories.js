// On each story page copy paste the code into the console and copy the object that is logged.

(function() {
    const slides = document.querySelectorAll('.slide');
    const results = [];
  
    slides.forEach(slide => {
      // Find the meta section where date, heading, and text are stored
      const metaContent = slide.querySelector('.slide-meta-content');
      if (!metaContent) return;
  
      // Extract the date
      const dateEl = slide.querySelector('.slide-meta h1 span');
      const date = dateEl ? dateEl.innerText.trim() : '';
  
      // Extract the heading
      const headingEl = metaContent.querySelector('p strong');
      const heading = headingEl ? headingEl.innerText.trim() : '';
  
      // Extract paragraphs (found inside the div[ng-bind-html])
      const paragraphContainer = metaContent.querySelector('div[ng-bind-html]');
      const paragraphs = paragraphContainer
        ? Array.from(paragraphContainer.querySelectorAll('p'))
            .map(p => p.innerText.trim())
            .filter(Boolean)
        : [];
  
      // Extract record IDs (from item-id elements)
      const recordIdEls = slide.querySelectorAll('.pure-u-8-24.shadow .item-id.ng-binding');
      const recordIds = Array.from(recordIdEls).map(el => el.innerText.replace('Arkiv-id:', '').trim());
  
      results.push({ date, heading, paragraphs, recordIds });
    });
  
    console.log(results);
  })();