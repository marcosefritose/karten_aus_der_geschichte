<script>
  // @ts-ignore
  import Carousel from 'svelte-carousel';
  import { browser } from '$app/environment';

  let carousel;
  let page = 0;
  let hoverLaunch = false;

  const slider_info = [
    {
      title: 'Wo hat Geschichte stattgefunden?',
      description:
        'Entdecke alle Schauplätze der Weltgeschichte auf einen Blick. Eine interaktive Karte ermöglicht es dir, alle in den Podcasts besprochenen geschichtsträchtigen Orte zu erkunden.'
    },
    {
      title: 'Worum geht es überhaupt?',
      description:
        'Themen und Inhalte eines oder mehrerer Podcasts in einem einzigen Graph zusammengefasst. So hast du Zusammenhänge und Referenzen immer im Blick.'
    },
    {
      title: 'Wann war das doch gleich?',
      description:
        'Ein Schritt nach dem anderen. Alle besprochenen Ereignisse auf einem Zeitstrahl. So kannst du Inhalte chronologisch nachvollziehen und Zusammenhänge besser verstehen.'
    }
  ];
</script>

<div
  class="bg-pod-dark from-pod-primary to-pod-dark to-25% font-space relative h-screen w-screen bg-gradient-to-b px-5 pb-20 text-white sm:pb-0"
>
  <!-- Background stars -->
  <img src="/stars_tl.svg" alt="" class="pointer-events-none absolute left-0 top-0 p-5" />
  <img src="/stars_tl.svg" alt="" class="pointer-events-none absolute bottom-0 right-0 p-5" />

  <!-- Title + Subtitle with Elipses Background -->
  <div
    class="bg-elipse mx-auto flex h-2/3 max-w-3xl flex-col items-center justify-center bg-contain bg-center bg-no-repeat px-6"
  >
    <h1 class="py-2 text-center text-5xl sm:text-6xl">Podiverse</h1>
    <h2 class="text-center text-lg sm:text-xl">Entdecke das Podcast Universum mit uns!</h2>
  </div>
  <div class="h-1/3 w-full text-center">
    <p class="mx-auto max-w-lg text-lg">
      Nimm jetzt an unserer Umfrage teil und hilf uns dabei, deine Podcasterfahrung zu verbessern!
    </p>
    <a
      href="https://forms.gle/z7AvjnwXHsGPbtjJ8"
      target="_blank"
      rel="noopener noreferrer"
      class="hover:bg-secondary bg-pod-primary my-4 inline-block rounded-xl px-8 py-4 text-xl text-white transition duration-500 ease-in-out hover:scale-125"
    >
      Umfrage
    </a>
  </div>
</div>

<div
  class="bg-pod-dark w-screen bg-[url('/waves_top.svg')] bg-contain bg-bottom bg-no-repeat px-5 pb-80 text-white"
>
  <!-- Caroussel -->
  {#if browser}
    <div class="mt relative mx-auto w-full pt-20 text-center">
      <!-- Info Box -->
      <div
        class="font-space text-pod-light absolute -top-5 left-0 z-40 w-4/5 transform rounded-3xl bg-black px-4 py-3 text-left md:w-1/2 md:translate-x-0 md:px-6 md:py-5 lg:w-1/3 xl:left-20"
      >
        <h2 class="text-md mb-2 underline underline-offset-1 sm:text-lg md:text-xl">
          {slider_info[page].title}
        </h2>
        <p class="md:text-md text-sm">{slider_info[page].description}</p>
      </div>

      <!-- Carousel Slider -->
      <Carousel
        autoplay
        autoplayDuration={10000}
        autoplayProgressVisible
        bind:this={carousel}
        on:pageChange={(/** @type {{ detail: number; }} */ event) => (page = event.detail)}
      >
        <div
          class="h-[20rem] bg-[url('/kag_demo.gif')] bg-contain bg-center bg-no-repeat sm:h-[24rem] md:h-[36rem]"
        />
        <div
          class="h-[20rem] bg-[url('/graph_demo.gif')] bg-contain bg-center bg-no-repeat sm:h-[24rem] md:h-[36rem]"
        />
        <div
          class="h-[20rem] bg-[url('/timeline_demo.gif')] bg-contain bg-center bg-no-repeat sm:h-[24rem] md:h-[36rem]"
        />
      </Carousel>
    </div>
  {/if}
</div>

<div class="font-space w-screen bg-black px-5 text-center text-white">
  <h2 class="py-8 text-3xl">Wie es funktioniert</h2>
  <div class="flex justify-center gap-2">
    <img src="/process_animation.svg" alt="" class="w-1/4 sm:w-auto" />
    <div class="my-auto max-w-lg text-left text-xs sm:text-base">
      <p class="py-2 sm:py-4 md:py-6">
        Alles beginnt mit Podcastern, die das tun, was sie am besten können: Podcasts produzieren.
        Wir kümmern uns um den Rest. Alles was wir dafür brauchen, ist der Link zu deinem Feed.
        Dabei ist es egal, wie du deinen Podcast produzierst oder wo du ihn hostest.
      </p>
      <p class="py-2 sm:py-4 md:py-6">
        Du entscheidest frei, welche Informationen für deinen Podcast am relevantesten sind. Dabei
        können zum Beispiel besprochene <span class="bg-badge-blue rounded-lg bg-opacity-50 px-1"
          >Orte</span
        >, behandelte <span class="bg-badge-red rounded-lg bg-opacity-50 px-1">Themen</span> oder
        <span class="bg-badge-green rounded-lg bg-opacity-50 px-1">Personen</span> automatisch identifiziert
        werden.
      </p>
      <p class="py-2 sm:py-4 md:py-6">
        Wir extrahieren die Informationen und reichern sie mit zusätzlichen hilfreichen Daten an.
      </p>
      <p class="py-2 sm:py-4 md:py-6">
        Wähle aus verschiedenen Möglichkeiten, deine Daten zu visualisieren. Integriere sie in deine
        Website oder lass uns den Hosting übernehmen.
      </p>
      <p class="py-2 sm:py-4 md:py-6">
        Du hast eine bessere Idee, was du mit den Daten machen kannst? Nutze unsere API und
        erstellte Transkripte und entwickle deine eigenen Anwendungen.
      </p>
    </div>
  </div>
</div>

<div
  class="bg-pod-dark flex w-screen flex-col items-center bg-[url('/waves_bottom.svg')] bg-contain bg-top bg-no-repeat pt-80"
>
  <img src="/rocket.svg" class="mb-10 w-20 {hoverLaunch ? 'animate-reverse-bounce' : ''}" />
  <div
    class=" bg-pod-dark font-space flex h-64 w-full flex-col items-center justify-center bg-[url('/launch_pad.svg')] bg-cover bg-top bg-no-repeat px-4 text-center"
  >
    <a
      href="/demo"
      target="_blank"
      rel="noopener noreferrer"
      class="hover:bg-secondary bg-pod-dark mx-auto my-4 rounded-xl px-8 py-4 text-xl text-white transition duration-500 ease-in-out hover:scale-125"
      on:mouseenter={() => (hoverLaunch = true)}
      on:mouseleave={() => (hoverLaunch = false)}
    >
      Launch Demo
    </a>
    <p>
      Wir sind noch in der Entwicklung, aber du kannst schon mal einen Blick auf unsere Demo werfen.
    </p>
  </div>
</div>
