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
    <h2 class="text-center text-xl">Lift your podcast to the next level.</h2>
    <img src="/animation.svg" alt="" class="z-10" />
    <div class="z-20 mb-20 flex max-w-6xl flex-col gap-5 px-4 lg:-mt-20 lg:flex-row">
      <div class="text-center">
        <h3 class="bg-grayish shadow-no-blur mx-auto w-64 rounded rounded-2xl py-4 text-xl">
          Transcribe
        </h3>

        <p class="w-fit px-2 py-4 font-sans">
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Ex dolorum, omnis in eaque
          explicabo ratione, debitis fugiat reprehenderit praesentium tempora exercitationem. Maxime
          architecto facere veritatis doloremque repellat atque est cumque.
        </p>
      </div>
      <div class="text-center">
        <h3
          class="bg-grayish shadow-no-blur mx-auto w-64 rounded rounded-2xl py-4 text-center text-xl"
        >
          Extract
        </h3>

        <p class="w-fit px-2 py-4 font-sans">
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Ex dolorum, omnis in eaque
          explicabo ratione, debitis fugiat reprehenderit praesentium tempora exercitationem. Maxime
          architecto facere veritatis doloremque repellat atque est cumque.
        </p>
      </div>
      <div class="text-center">
        <h3
          class="bg-grayish shadow-no-blur mx-auto w-64 rounded rounded-2xl py-4 text-center text-xl"
        >
          Visualize
        </h3>

        <p class="w-fit px-2 py-4 font-sans">
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Ex dolorum, omnis in eaque
          explicabo ratione, debitis fugiat reprehenderit praesentium tempora exercitationem. Maxime
          architecto facere veritatis doloremque repellat atque est cumque.
        </p>
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
