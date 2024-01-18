<script>
  import { page } from '$app/stores';
  import ListIcon from '../../components/icons/ListIcon.svelte';
  import DashboardIcon from '../../components/icons/DashboardIcon.svelte';
  import PinpointIcon from '../../components/icons/PinpointIcon.svelte';
  import TopicIcon from '../../components/icons/TopicIcon.svelte';
  import SettingsIcon from '../../components/icons/SettingsIcon.svelte';
</script>

<div class="flex h-screen">
  <nav class="bg-gag-white flex h-screen w-72 flex-col gap-2">
    <a href="/dashboard/episodes">
      <img src="/gag_logo.png" class="h-18 mx-auto w-44 object-contain" alt="" />
    </a>
    <!-- <a href="/dashboard">
      <div
        class="mx-4 flex cursor-pointer items-center rounded-lg p-2 {$page.url.pathname ==
        '/dashboard'
          ? 'bg-gag-primary text-gag-white'
          : 'bg-gag-white'}"
      >
        <DashboardIcon fill="currentColor" />
        <span class="px-2">Overview</span>
      </div>
    </a> -->
    <a href="/dashboard/episodes">
      <div
        class="mx-4 flex cursor-pointer items-center rounded-lg p-2 {$page.url.pathname ==
        '/dashboard/episodes'
          ? 'bg-gag-primary text-gag-white'
          : 'bg-gag-white'}"
      >
        <ListIcon fill="currentColor" />
        <span class="px-2">Episoden</span>
      </div>
    </a>

    <a href="/dashboard/locations">
      <div
        class="mx-4 flex cursor-pointer items-center rounded-lg p-2 {$page.url.pathname ==
        '/dashboard/locations'
          ? 'bg-gag-primary text-gag-white'
          : 'bg-gag-white'}"
      >
        <PinpointIcon fill="currentColor" />
        <span class="px-2">Orte</span>
      </div>
    </a>
    <a href="/dashboard/topics">
      <div
        class="mx-4 flex cursor-pointer items-center rounded-lg p-2 {$page.url.pathname ==
        '//dashboard/topics'
          ? 'bg-gag-primary text-gag-white'
          : 'bg-gag-white'}"
      >
        <TopicIcon fill="currentColor" />
        <span class="px-2">Themen</span>
      </div>
    </a>

    <a href="/" class="">
      <div class="mx-4 flex cursor-pointer items-center rounded-lg p-2">
        <img class="h-8 w-8 rounded-t-md" src="../../icons/map.svg" alt="Map Icon" />
        <span class="px-2">zur Karte</span>
      </div>
    </a>
    <a href="//dashboard/settings" class="">
      <div
        class="mx-4 flex cursor-pointer items-center rounded-lg p-2 {$page.url.pathname ==
        '//dashboard/settings'
          ? 'bg-gag-primary text-gag-white'
          : 'bg-gag-white'}"
      >
        <SettingsIcon fill="currentColor" />

        <span class="px-2">Einstellung</span>
      </div>
    </a>
  </nav>

  <slot />
</div>
