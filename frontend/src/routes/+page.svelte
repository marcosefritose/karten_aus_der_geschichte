<script>
  import MailchimpForm from '../components/MailchimpForm.svelte';
</script>

<div class="relative h-screen w-screen overflow-x-hidden">
  <img
    src="/logo_full.svg"
    alt="Podmap Logo"
    class="absolute left-1/2 top-20 z-20 w-72 -translate-x-1/2 transform overflow-auto transition duration-500 ease-in-out hover:scale-110 sm:top-16 sm:w-80"
  />
  <img
    src="/rays.svg"
    alt=""
    class="absolute left-1/2 h-full w-fit -translate-x-1/2 transform object-none object-top sm:min-h-fit sm:min-w-fit"
  />

  <div class="font-tiro flex flex-col items-center pt-[23rem]">
    <h1 class="text-center text-7xl sm:text-8xl">podiverse</h1>
    <h2 class="z-30 mt-20 px-2 text-center text-3xl sm:text-4xl">
      Wir bringen Podcasts zum Leben und<br /> machen Schluss mit langweiligen Feeds, Charts & Suchfunktionen!
    </h2>
    <img
      src="/animation.svg"
      alt=""
      class="absolute top-20 left-0 z-0 hidden h-full w-full object-none object-center sm:block"
    />
    <div class="z-20 mt-24 mb-20 max-w-6xl px-4 sm:mt-60">
      <h1 class="mb-16 px-4 text-center text-5xl sm:text-6xl">So funktioniert's!</h1>
      <div class="flex flex-col gap-5 lg:flex-row">
        <div class="flex-1 text-center">
          <h3 class="bg-grayish shadow-no-blur mx-auto w-64 rounded rounded-2xl py-4 text-xl">
            Transkribieren
          </h3>

          <p class="w-fit px-2 py-4 font-sans">
            Wir hören genau hin! Mit Hilfe von KI transkribieren wir Episoden und machen sie
            durchsuchbar. Damit können wir alle Informationen aus den Episoden nutzen und sind nicht
            auf die manuell erstellten Beschreibungen & Tags angewiesen.
          </p>
        </div>
        <div class="flex-1 text-center">
          <h3
            class="bg-grayish shadow-no-blur mx-auto w-64 rounded rounded-2xl py-4 text-center text-xl"
          >
            Extrahieren
          </h3>

          <p class="w-fit px-2 py-4 font-sans">
            Jeder entscheidest selbst, welche Informationen für einen Podcast wichtig sind, egal ob
            besprochene Personen, Orte oder Themen. Wir extrahieren diese Informationen und reichern
            sie mit weiteren relevanten Daten an. So können wir gesamte Podcasts strukturieren und
            durchsuchbar machen.
          </p>
        </div>
        <div class="flex-1 text-center">
          <h3
            class="bg-grayish shadow-no-blur mx-auto w-64 rounded rounded-2xl py-4 text-center text-xl"
          >
            Visualisieren
          </h3>

          <p class="w-fit px-2 py-4 font-sans">
            Mit unseren bereitgestellten interaktiven Visualisierungen bringen wir deinen Podcast
            zum Leben. So können Hörer:innen auf eine ganz neue Art und Weise Folgen entdecken und
            erleben. Du hast selber noch eine bessere Idee? Nutze die API und rücke Inhalte ins
            beste Licht!
          </p>
        </div>
      </div>
    </div>
  </div>

  <div class="mb-20 flex w-full items-center">
    <a
      href="/demo"
      target="_blank"
      rel="noopener noreferrer"
      class="bg-primary shadow-no-blur hover:bg-secondary z-20 mx-auto rounded-xl px-8 py-4 text-4xl text-white transition duration-500 ease-in-out hover:scale-125"
    >
      Demo
    </a>
  </div>

  <div class="bg-grayish w-full">
    <MailchimpForm />
  </div>
</div>
