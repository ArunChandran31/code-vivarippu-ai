<template>
  <div style="padding-top:10px;">
    <div class="review-wrapper">
      <div class="controls-row">
        <div class="control-pill">Model:
          <select v-model="model">
            <option value="gpt">GPT-4.1</option>
            <option value="claude">Claude</option>
          </select>
        </div>

        <div class="control-pill">Language:
          <select v-model="languageOverride">
            <option value="">Auto</option>
            <option value="python">Python</option>
            <option value="javascript">JavaScript</option>
          </select>
        </div>

        <div class="control-pill" style="margin-left:auto;">all the drop down menu like programming language and other necessary ones are done in these grey boxes</div>
      </div>

      <div class="columns">
        <div class="code-box">
          <pre v-if="code" class="whitespace-pre-wrap">{{ code }}</pre>
          <div v-else style="color:#777">i want the code to be shown here in this box</div>
        </div>
        <div class="report-box">
          <div v-if="!review">All the report like the time complexity, space complexity, etc come here in this box.</div>
          <div v-else> ... show report ... </div>
        </div>
      </div>
    </div>
  </div>
</template>
