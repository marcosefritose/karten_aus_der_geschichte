<script>
  import { page } from '$app/stores';
</script>

<div class="flex h-screen">
  <nav class="bg-gag-light flex h-screen w-72 flex-col gap-2">
    <a href="/dashboard">
      <img src="/gag_logo.png" class="h-18 mx-auto w-44 object-contain" alt="" />
    </a>
    <a href="/dashboard">
      <div
        class="mx-4 flex cursor-pointer items-center rounded-lg p-2 {$page.url.pathname ==
        '/dashboard'
          ? 'bg-gag-white'
          : 'bg-light'}"
      >
        <img class="h-8 w-8 rounded-t-md" src="../icons/overview.svg" alt="Episode List Icon" />
        <span class="px-2">Overview</span>
      </div>
    </a>
    <a href="/dashboard/episodes">
      <div
        class="mx-4 flex cursor-pointer items-center rounded-lg p-2 {$page.url.pathname ==
        '/dashboard/episodes'
          ? 'bg-gag-white'
          : 'bg-light'}"
      >
        <img class="h-8 w-8 rounded-t-md" src="../icons/list.svg" alt="Episode List Icon" />
        <span class="px-2">Episoden</span>
      </div>
    </a>

    <a href="/dashboard/locations">
      <div
        class="mx-4 flex cursor-pointer items-center rounded-lg p-2 {$page.url.pathname ==
        '/dashboard/locations'
          ? 'bg-gag-white'
          : 'bg-light'}"
      >
        <img class="h-8 w-8 rounded-t-md" src="../icons/location.svg" alt="Location List Icon" />
        <span class="px-2">Orte</span>
      </div>
    </a>
    <a href="/dashboard/topics">
      <div
        class="mx-4 flex cursor-pointer items-center rounded-lg p-2 {$page.url.pathname ==
        '/dashboard/topics'
          ? 'bg-gag-white'
          : 'bg-light'}"
      >
        <img class="h-8 w-8 rounded-t-md" src="../icons/topic.svg" alt="Episode Topics Icon" />
        <span class="px-2">Themen</span>
      </div>
    </a>

    <a href="/" class="">
      <div class="mx-4 flex cursor-pointer items-center rounded-lg p-2">
        <img class="h-8 w-8 rounded-t-md" src="../icons/map.svg" alt="Map Icon" />
        <span class="px-2">zur Karte</span>
      </div>
    </a>
    <a href="/dashboard/settings" class="">
      <div class="mx-4 flex cursor-pointer items-center rounded-lg p-2">
        <img class="h-8 w-8 rounded-t-md" src="../icons/settings.svg" alt="Map Icon" />
        <span class="px-2">Einstellung</span>
      </div>
    </a>
  </nav>

  <slot />
</div>
