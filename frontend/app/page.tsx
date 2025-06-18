import ChatWidget from "@/components/chat-widget";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gray-50">
      <div className="text-center max-w-3xl">
        <h1 className="text-4xl font-bold mb-4">Portail de la Faculté</h1>
        <p className="text-gray-600 mb-8">
          Bienvenue sur le portail de la faculté. Utilisez l'assistant de chat
          dans le coin inférieur droit pour obtenir de l'aide.
        </p>
      </div>
      <ChatWidget />
    </main>
  );
}
