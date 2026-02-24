import Markdown from "react-markdown";

interface Props {
  content: string;
  loading: boolean;
  error: string;
}

export default function AnalysisResult({ content, loading, error }: Props) {
  if (error) {
    return (
      <div className="rounded-md bg-red-50 border border-red-200 p-4 text-red-700">
        {error}
      </div>
    );
  }

  if (!content && !loading) {
    return (
      <p className="text-gray-400 italic text-center py-8">
        Select a strategy and click &quot;Analyze Portfolio&quot; to get AI
        suggestions.
      </p>
    );
  }

  return (
    <div className="prose prose-sm max-w-none">
      <Markdown>{content}</Markdown>
      {loading && (
        <span className="inline-block w-2 h-4 bg-blue-500 animate-pulse ml-0.5" />
      )}
    </div>
  );
}
