<script>
  import { page } from '$app/stores';
</script>

<div class="flex">
  <nav class="bg-gag-light flex h-screen w-1/6 flex-col gap-2">
    <a href="/dashboard">
      <img src="/gag_logo.png" class="mx-auto w-56 object-contain" alt="" />
    </a>
    <a href="/dashboard/episodes">
      <div
        class="mx-4 flex cursor-pointer items-center rounded-lg p-2 {$page.url ==
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
        class="mx-4 flex cursor-pointer items-center rounded-lg p-2 {$page.url ==
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
        class="mx-4 flex cursor-pointer items-center rounded-lg p-2 {$page.url ==
        '/dashboard/topics'
          ? 'bg-gag-white'
          : 'bg-light'}"
      >
        <img class="h-8 w-8 rounded-t-md" src="../icons/topic.svg" alt="Episode Topics Icon" />
        <span class="px-2">Themen</span>
      </div>
    </a>
  </nav>

  <slot />
</div>
